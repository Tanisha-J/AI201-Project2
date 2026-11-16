#!/usr/bin/env python3
"""
Where does the time go in one FitFindr run?  ← CAPSTONE STRETCH: latency breakdown

    python latency_breakdown.py              5 matching queries x 3 rounds = 15 runs
    python latency_breakdown.py --rounds 1   quicker: 5 runs

Runs the five matching queries from scenarios.py with the cache OFF (so every
model call is real), reads session["timings"] that run_agent() records, and
prints a per-stage table. It also writes the table and every raw run to
results/latency_<timestamp>.md, ready to commit and paste into the README.

Stages, in the order a run goes through them:

    parse_query           regex, in-process
    search_listings_mcp   the search tool, called over MCP. This includes
                          starting mcp_server.py as a fresh Python process
    suggest_outfit        model call #1
    create_fit_card       model call #2

Two extra columns separate time that isn't really "the stage":

    rate_limit_wait       time asleep in generate.py waiting for a free slot
                          (15 requests/minute) or backing off after a 429.
                          It's counted inside the model stages, and shown
                          here too so you can see how much of a stage it was.
    mcp_overhead          search_listings_mcp minus the same search run
                          in-process. That's the cost of the extra process,
                          not the search.

Rate-limit waits are real latency a user feels, so they stay in the totals.
The script waits a little between runs (--gap) so the pacing in generate.py
doesn't hide the model's own speed. Two model calls per run x 15 runs fits
under 15/min only if the runs are spread out.
"""

import argparse
import contextlib
import datetime as dt
import io
import statistics
import time
from pathlib import Path

import config
import trace
from agent import run_agent
from scenarios import SCENARIOS
from tools import search_listings
from utils.data_loader import get_example_wardrobe

STAGES = ["parse_query", "search_listings_mcp", "suggest_outfit", "create_fit_card"]
QUERIES = [s["query"] for s in SCENARIOS if s.get("criterion") == "3+4"]


def _direct_search_ms(parsed: dict) -> float:
    start = time.perf_counter()
    search_listings(parsed["description"], parsed["size"], parsed["max_price"])
    return (time.perf_counter() - start) * 1000


def _summary(values: list[float]) -> str:
    if not values:
        return "| — | — | — | — |"
    return (f"| {statistics.mean(values):,.0f} | {statistics.median(values):,.0f} "
            f"| {min(values):,.0f} | {max(values):,.0f} |")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--rounds", type=int, default=3, help="times to run all five queries")
    ap.add_argument("--gap", type=float, default=8.0,
                    help="seconds to pause between runs (keeps under the rate limit)")
    args = ap.parse_args()

    config.CACHE_ENABLED = False  # every model call must be real
    wardrobe = get_example_wardrobe()

    rows = []  # one dict per run
    total_runs = args.rounds * len(QUERIES)
    n = 0
    for rnd in range(1, args.rounds + 1):
        for query in QUERIES:
            n += 1
            print(f"[{n}/{total_runs}] round {rnd}: {query!r}", flush=True)
            trace.start_trace()
            with contextlib.redirect_stdout(io.StringIO()):  # trace prints every step
                session = run_agent(query, wardrobe)
            t = dict(session["timings"])
            t["query"] = query
            t["round"] = rnd
            t["error"] = session["error"]
            t["direct_search"] = _direct_search_ms(session["parsed"])
            if "search_listings_mcp" in t:
                t["mcp_overhead"] = t["search_listings_mcp"] - t["direct_search"]
            t["rate_limit_wait"] = sum(v for k, v in t.items()
                                       if isinstance(k, str) and k.endswith(".rate_limit_wait"))
            rows.append(t)
            print(f"      total {t['total']:,.0f} ms"
                  + (f"   error: {t['error'][:70]}" if t["error"] else ""), flush=True)
            if n < total_runs:
                time.sleep(args.gap)

    ok = [r for r in rows if not r["error"]]
    out = []
    out.append(f"# Latency breakdown — {dt.datetime.now():%Y-%m-%d %H:%M}")
    out.append("")
    out.append(f"Model `{config.MODEL}`, cache off, {len(rows)} runs "
               f"({args.rounds} rounds x {len(QUERIES)} matching queries), "
               f"{args.gap:g}s gap between runs. Stats over the {len(ok)} runs "
               f"that completed all three tools. All times in ms, wall clock "
               f"(`time.perf_counter`), recorded by `agent._timed()`.")
    out.append("")
    out.append("| Stage | Mean | Median | Min | Max | Share of mean total |")
    out.append("|---|---|---|---|---|---|")
    mean_total = statistics.mean(r["total"] for r in ok) if ok else 0
    for stage in STAGES + ["total"]:
        vals = [r[stage] for r in ok if stage in r]
        share = (f"{statistics.mean(vals) / mean_total:.1%}" if vals and mean_total else "—")
        out.append(f"| {stage} " + _summary(vals) + f" {share} |")
    out.append("| *of which: rate_limit_wait* " + _summary([r["rate_limit_wait"] for r in ok])
               + " — |")
    out.append("| *search, in-process (no MCP)* " + _summary([r["direct_search"] for r in ok])
               + " — |")
    out.append("| *MCP overhead (mcp − in-process)* "
               + _summary([r["mcp_overhead"] for r in ok if "mcp_overhead" in r]) + " — |")
    unaccounted = [r["total"] - sum(r.get(s, 0) for s in STAGES) for r in ok]
    out.append("| *unaccounted (loop glue, trace)* " + _summary(unaccounted) + " — |")
    out.append("")
    out.append("## Every run")
    out.append("")
    out.append("| # | Round | Query | " + " | ".join(STAGES) + " | wait | total | error |")
    out.append("|---|---|---|" + "---|" * (len(STAGES) + 3))
    for i, r in enumerate(rows, 1):
        cells = [f"{r[s]:,.1f}" if s in r else "—" for s in STAGES]
        out.append(f"| {i} | {r['round']} | {r['query']} | " + " | ".join(cells)
                   + f" | {r['rate_limit_wait']:,.0f} | {r['total']:,.0f} | {r['error'] or ''} |")

    text = "\n".join(out) + "\n"
    print("\n" + text)
    path = Path(config.ROOT) / "results" / f"latency_{dt.datetime.now():%Y-%m-%d_%H%M}.md"
    path.write_text(text, encoding="utf-8")
    print(f"Written to {path.relative_to(config.ROOT)} — commit it.")


if __name__ == "__main__":
    main()
