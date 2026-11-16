#!/usr/bin/env python3
"""
Run the capstone trials against the real server. ← CAPSTONE

    python capstone_trials.py --label before       three trials (the default)
    python capstone_trials.py --label after --trials 3

One trial is exactly the set defined in criteria.md (capstone section):

  1. start `serve.py` with the real key, logging to a fresh file
  2. 10 matching queries (the five examples, twice each), 6 s pause after each
     2 impossible queries, 2 no-item queries, 5 malformed bodies
  3. stop it; start `serve.py` with GEMINI_API_KEY=not-a-real-key, same log
  4. 5 x 'denim jacket under $50'; stop it

Requests go through curl, so the client-side time is curl's `time_total`,
which is what criteria C2 and C3 name. Scores for C1–C5 are computed
mechanically from the criteria's own definitions, and the raw evidence (status,
time, X-Request-ID, the log lines) is written next to them so every verdict can
be checked by hand.

Writes results/capstone_<label>.md and results/capstone_logs/<label>_trial<N>.jsonl.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PY = sys.executable
PORT_GOOD, PORT_BAD = 5060, 5061

MATCHING = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
]
IMPOSSIBLE = ["designer ballgown size XXS under $5", "gold sequin gown size 2 under $3"]
NO_ITEM = ["size W30", "under $30 size M"]
MALFORMED = [  # (label, raw body or None for no body at all)
    ("no body", None),
    ("{}", "{}"),
    ('{"query": ""}', '{"query": ""}'),
    ('{"query": 42}', '{"query": 42}'),
    ('["denim jacket"]', '["denim jacket"]'),
]
BAD_KEY_QUERY = "denim jacket under $50"
PAUSE_AFTER_COMPLETED = 6.0

FIELDS = ["ts", "request_id", "route", "query", "wardrobe", "status", "outcome",
          "error", "selected_item", "fit_card_chars", "queued_ms", "agent_ms",
          "duration_ms", "timings", "model_calls", "cache_hits", "tokens_prompt",
          "tokens_output", "tokens_total"]


# ── server and requests ───────────────────────────────────────────────────────

def start_server(port: int, log_path: Path, bad_key: bool) -> subprocess.Popen:
    env = dict(os.environ, PORT=str(port), FITFINDR_LOG=str(log_path))
    if bad_key:
        env["GEMINI_API_KEY"] = "not-a-real-key"
    proc = subprocess.Popen([PY, "serve.py"], cwd=ROOT, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        try:
            urllib.request.urlopen(f"http://localhost:{port}/health", timeout=1)
            return proc
        except Exception:  # noqa: BLE001 — not up yet
            time.sleep(0.5)
    proc.kill()
    raise RuntimeError(f"serve.py didn't come up on port {port}")


def stop_server(proc: subprocess.Popen) -> None:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def curl(port: int, body: str | None) -> dict:
    """POST /ask with curl. Returns status, time_total, request id and parsed body."""
    with tempfile.TemporaryDirectory() as tmp:
        headers, out = Path(tmp) / "h", Path(tmp) / "b"
        cmd = ["curl", "-s", "-X", "POST", f"http://localhost:{port}/ask",
               "-D", str(headers), "-o", str(out), "-w", "%{http_code} %{time_total}"]
        if body is not None:
            cmd += ["-H", "Content-Type: application/json", "-d", body]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        code, seconds = result.stdout.split()
        request_id = None
        for line in headers.read_text(errors="replace").splitlines():
            if line.lower().startswith("x-request-id:"):
                request_id = line.split(":", 1)[1].strip()
        raw = out.read_text(errors="replace")
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None
    return {"status": int(code), "time_ms": float(seconds) * 1000,
            "request_id": request_id, "json": parsed, "raw": raw[:300]}


def run_trial(n: int, label: str) -> list[dict]:
    log_dir = ROOT / "results" / "capstone_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{label}_trial{n}.jsonl"
    log_path.unlink(missing_ok=True)

    sent = []

    def send(port, kind, body, shown):
        r = curl(port, body)
        r.update(kind=kind, sent=shown)
        sent.append(r)
        print(f"  trial {n}  {kind:10} {r['status']}  {r['time_ms']:8,.0f} ms  {shown}", flush=True)
        return r

    proc = start_server(PORT_GOOD, log_path, bad_key=False)
    try:
        for q in MATCHING * 2:
            send(PORT_GOOD, "matching", json.dumps({"query": q}), q)
            time.sleep(PAUSE_AFTER_COMPLETED)
        for q in IMPOSSIBLE:
            send(PORT_GOOD, "impossible", json.dumps({"query": q}), q)
        for q in NO_ITEM:
            send(PORT_GOOD, "no_item", json.dumps({"query": q}), q)
        for shown, body in MALFORMED:
            send(PORT_GOOD, "malformed", body, shown)
    finally:
        stop_server(proc)

    proc = start_server(PORT_BAD, log_path, bad_key=True)
    try:
        for _ in range(5):
            send(PORT_BAD, "bad_key", json.dumps({"query": BAD_KEY_QUERY}), BAD_KEY_QUERY)
    finally:
        stop_server(proc)

    records = [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]
    by_id = {}
    for rec in records:
        by_id.setdefault(rec.get("request_id"), []).append(rec)
    for r in sent:
        r["log"] = by_id.get(r["request_id"], [])
    return sent


# ── scoring, straight from the criteria's wording ─────────────────────────────

def c1(r):
    if len(r["log"]) != 1:
        return False, f"{len(r['log'])} log lines for id {r['request_id']}"
    rec = r["log"][0]
    missing = [f for f in FIELDS if f not in rec]
    if missing:
        return False, f"missing fields {missing}"
    if rec["status"] != r["status"]:
        return False, f"logged status {rec['status']} != HTTP {r['status']}"
    return True, ""


def c2(r):
    if len(r["log"]) != 1:
        return False, "no single log record"
    rec = r["log"][0]
    why = []
    if rec["outcome"] != "completed":
        why.append(f"outcome {rec['outcome']}")
    gap = abs(r["time_ms"] - rec["duration_ms"])
    if gap > 250:
        why.append(f"curl {r['time_ms']:,.0f} vs logged {rec['duration_ms']:,.0f} ms (gap {gap:,.0f})")
    if rec["model_calls"] != 2:
        why.append(f"model_calls {rec['model_calls']}")
    if not rec["tokens_total"] > 0:
        why.append("tokens_total 0")
    return not why, "; ".join(why) or f"gap {gap:,.0f} ms, {rec['tokens_total']} tokens"


def c3(r):
    why = []
    if r["time_ms"] >= 5000:
        why.append(f"{r['time_ms']:,.0f} ms")
    err = (r["json"] or {}).get("error") or ""
    if "API key" not in err:
        why.append("error doesn't mention 'API key'")
    rec = r["log"][0] if len(r["log"]) == 1 else {}
    if rec.get("outcome") != "model_unavailable":
        why.append(f"logged outcome {rec.get('outcome')}")
    if rec.get("tokens_total") != 0:
        why.append(f"tokens_total {rec.get('tokens_total')}")
    return not why, "; ".join(why) or f"{r['time_ms']:,.0f} ms"


def c4(r):
    ok = r["status"] == 400 and isinstance(r["json"], dict) and bool(r["json"].get("error"))
    return ok, f"HTTP {r['status']}" + ("" if ok else f": {(r['json'] or {}).get('error', r['raw'])[:90]}")


def c5(r):
    rec = r["log"][0] if len(r["log"]) == 1 else None
    if not rec or rec["outcome"] != "completed":
        return False, "did not complete"
    return rec["duration_ms"] <= 10000, f"{rec['duration_ms']:,.0f} ms"


CRITERIA = [
    ("C1. Every request leaves exactly one complete log record", "24 of 24", lambda s: s, c1, 24),
    ("C2. Logged numbers match (±250 ms, 2 calls, tokens > 0)", "10 of 10",
     lambda s: [r for r in s if r["kind"] == "matching"], c2, 10),
    ("C3. Dead key: < 5 s, says 'API key', logged model_unavailable", "5 of 5",
     lambda s: [r for r in s if r["kind"] == "bad_key"], c3, 5),
    ("C4. Malformed requests get a 400, never a 500", "5 of 5",
     lambda s: [r for r in s if r["kind"] == "malformed"], c4, 5),
    ("C5. Warm completed runs ≤ 10,000 ms", "9 of 10",
     lambda s: [r for r in s if r["kind"] == "matching"], c5, 9),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()

    trials = []
    for n in range(1, args.trials + 1):
        print(f"\n=== trial {n} of {args.trials} ===", flush=True)
        trials.append(run_trial(n, args.label))

    out = [f"# Capstone run log — {args.label}", "",
           f"{dt.datetime.now():%Y-%m-%d %H:%M}, `python capstone_trials.py --label {args.label}`. "
           f"{args.trials} trials of the 24-request set defined in criteria.md. "
           f"Raw logs: `results/capstone_logs/{args.label}_trial<N>.jsonl`.", "",
           "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1))
           + " | Verdict |",
           "|---|---|" + "---|" * args.trials + "---|"]
    details = []
    for name, target, pick, check, need in CRITERIA:
        cells, held = [], True
        for t in trials:
            rows = pick(t)
            results = [check(r) for r in rows]
            passed = sum(ok for ok, _ in results)
            cells.append(f"{passed}/{len(rows)}")
            held &= passed >= need
            details.append((name, trials.index(t) + 1, rows, results))
        out.append(f"| {name} | {target} | " + " | ".join(cells)
                   + f" | {'MET' if held else 'MISSED'} |")

    out += ["", "## Every scored request", ""]
    for name, n, rows, results in details:
        out.append(f"**{name} — trial {n}**")
        out.append("")
        for r, (ok, note) in zip(rows, results):
            out.append(f"- {'PASS' if ok else 'FAIL'} · {r['kind']} · `{r['sent']}` · HTTP {r['status']} "
                       f"· curl {r['time_ms']:,.0f} ms · id `{r['request_id']}` · {note}")
        out.append("")

    out += ["## Trial 1 log, verbatim", "", "```jsonl"]
    out += [json.dumps(rec, ensure_ascii=False) for r in trials[0] for rec in r["log"]]
    out += ["```", ""]

    path = ROOT / "results" / f"capstone_{args.label}.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print("\n" + "\n".join(out[:4 + 2 + len(CRITERIA) + 1]))
    print(f"\nWritten to {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
