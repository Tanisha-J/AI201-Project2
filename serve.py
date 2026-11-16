#!/usr/bin/env python3
"""
FitFindr over HTTP. ← UNIT 9

    python serve.py                       run it on your machine
    gunicorn serve:app                    run it the way a host runs it

Everything else in this repo exits after one command. A host has nothing to
keep running, so a command line cannot be deployed. This file is the smallest
thing that can: it starts a web server, waits, and hands each request to the
same `run_agent()` your CLI calls. **No new agent logic lives here.** If your
loop works from `python app.py ask`, it works from here; if it doesn't, fix it
there, not in this file.

Two routes:

    POST /ask       {"query": "vintage graphic tee under $30",
                     "wardrobe": {...}}     ← wardrobe is optional
    GET  /health    is it awake?

`/ask` returns the session dict from `run_agent()` as JSON, unchanged — the
same keys you print from the command line, including `error`. Read
`session["error"]` first, exactly as you do everywhere else.

It runs **one request at a time**, and one route is deliberately slower than a
web server has to be. The reason is worth reading before you deploy: see the
note above `_one_at_a_time` below — it also decides which gunicorn worker you
can use.

Capstone: every /ask request now writes one structured JSON record to
logs/requests.jsonl (override with FITFINDR_LOG). The fields are listed above
_write_log() below.
"""

import datetime as dt
import json
import os
import sys
import threading
import time
import uuid
from pathlib import Path

# config first, and before anything that talks to the model: it loads your .env
# and fixes the Windows console encoding for every module that imports it.
import config  # noqa: F401

from flask import Flask, jsonify, request

import generate
from agent import run_agent
from utils.data_loader import get_example_wardrobe

app = Flask(__name__)

# A running service answers with real model calls: fit cards should differ
# between users, and the token counts in the log should be what a request
# really cost. So the response cache is OFF here unless AI201_CACHE=1 is set
# explicitly. (The CLI keeps its cache-on default for cheap debugging.)
config.CACHE_ENABLED = os.getenv("AI201_CACHE", "0") == "1"


# ── structured request log ── CAPSTONE ────────────────────────────────────────
# One JSON object per line, one line per /ask request — successful, stopped
# early, rejected with a 400, or crashed with a 500. A failure that leaves no
# line is a failure nobody can find later, so the line is written in a
# `finally`, after the response is decided and before it is sent.
#
# Fields (every record has all of them; ones that don't apply are null):
#   ts               UTC time the request arrived, ISO 8601
#   request_id       also sent back as the X-Request-ID response header
#   route            "/ask"
#   query            what came in — the raw value, whatever its type
#   wardrobe         "example" (defaulted) or "custom" (sent in the body)
#   status           HTTP status returned
#   outcome          completed / no_item / no_results / search_unavailable /
#                    model_unavailable / bad_request / server_error
#   error            the error text returned to the caller, if any
#   selected_item    listing id the agent chose, if it got that far
#   fit_card_chars   length of the fit card, if one was written
#   queued_ms        time spent waiting for the one-at-a-time lock
#   agent_ms         time inside run_agent()
#   duration_ms      whole request, arrival to response
#   timings          run_agent's per-stage ms (see agent._timed)
#   model_calls      real model calls this request made
#   cache_hits       answers served from cache instead (0 unless AI201_CACHE=1)
#   tokens_prompt / tokens_output / tokens_total
#                    as reported by the service — the cost of this request

LOG_PATH = Path(os.getenv("FITFINDR_LOG", config.ROOT / "logs" / "requests.jsonl"))
_log_lock = threading.Lock()


def _write_log(record: dict) -> None:
    """Append one record. Logging must never take a request down with it."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False, default=repr)
        with _log_lock, open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [serve] could not write the request log: {exc}", file=sys.stderr, flush=True)
    print(
        f"  [log] {record['request_id']} {record['status']} {record['outcome']} "
        f"{record['duration_ms']:,.0f} ms  calls={record['model_calls']} "
        f"tokens={record['tokens_total']}",
        file=sys.stderr, flush=True,
    )


def _new_record(request_id: str) -> dict:
    return {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds"),
        "request_id": request_id,
        "route": "/ask",
        "query": None,
        "wardrobe": None,
        "status": None,
        "outcome": None,
        "error": None,
        "selected_item": None,
        "fit_card_chars": None,
        "queued_ms": None,
        "agent_ms": None,
        "duration_ms": None,
        "timings": None,
        "model_calls": 0,
        "cache_hits": 0,
        "tokens_prompt": 0,
        "tokens_output": 0,
        "tokens_total": 0,
    }


# ── one request at a time ─────────────────────────────────────────────────────
# Here's why this exists.
#
# A web server will happily run two requests at once. Two things in this repo
# assume otherwise:
#
#   • If you moved a tool onto MCP in unit 4, `mcp_client.call_tool` starts
#     `mcp_server.py` as a separate process over stdio, one per call. Two
#     overlapping requests means two extra Python interpreters, and the free
#     tier you're deploying to has 512 MB for all of it. That is the reason
#     that would still be here even if everything else were perfect.
#   • `generate.py`'s pacing window and its call counter are plain module
#     globals — deliberately, because that file is teaching pacing and quota,
#     not locking. Two threads sharing them means the per-minute limiter is
#     counting something that isn't true.
#
# What the lock covers is exactly the agent run: the part that spawns
# processes and calls the model. Reading the request, rejecting a bad one, and
# turning the answer into JSON all happen outside it — so a request with a
# malformed body comes straight back with a 400 instead of queueing behind
# somebody else's agent.
#
# Serialising the runs costs you nothing here — this is one user asking one
# question — and it keeps the deployed behaviour identical to the CLI's. When
# that stops being an acceptable trade, the fix is a real queue, not a bigger
# lock.
#
# The same constraint decides your start command, and this is the part that
# bites in deployment rather than on your machine. `mcp_client.call_tool`
# wraps `asyncio.run()`, and `asyncio.run()` refuses to start when an event
# loop is already running. An async worker always has one running. So under
# `gunicorn -k gevent` (or `-k eventlet`, or `serve:app` wrapped for an ASGI
# server like uvicorn) EVERY MCP call fails with "asyncio.run() cannot be
# called from a running event loop" — not some of them under load, all of
# them, every time, in a place your laptop never showed you.
#
#     gunicorn serve:app              ← right: the DEFAULT sync worker
#     gunicorn -k gevent serve:app    ← breaks every MCP call you make

_one_at_a_time = threading.Lock()


@app.get("/health")
def health():
    """Is the server awake? A host pings something like this to find out."""
    return jsonify({"status": "ok"})


@app.post("/ask")
def ask():
    """Run one /ask request and log it, however it ends. The work is in _ask."""
    request_id = uuid.uuid4().hex[:12]
    start = time.perf_counter()
    record = _new_record(request_id)
    status = 500  # until something decides otherwise
    try:
        response, status = _ask(record)
    except Exception as exc:  # noqa: BLE001 — logged, then a 500 with a sentence
        record["outcome"] = "server_error"
        record["error"] = f"{type(exc).__name__}: {exc}"
        response, status = jsonify({"error": record["error"]}), 500
    finally:
        # `finally` so even a failure inside the except above still logs.
        record["duration_ms"] = round((time.perf_counter() - start) * 1000, 1)
        record["status"] = status
        _write_log(record)
    response.headers["X-Request-ID"] = request_id
    return response, status


def _ask(record: dict):
    """
    Run the agent on one query.

    In:   {"query": "...", "wardrobe": {...}}   wardrobe optional — leave it
                                                out and you get the same
                                                example wardrobe the CLI uses.
    Out:  the session dict from run_agent(), as JSON.
    """
    payload = request.get_json(silent=True) or {}
    record["query"] = payload.get("query")
    query = (payload.get("query") or "").strip()
    if not query:
        # 400 rather than a stack trace: the caller can act on this one.
        message = ("Send JSON with a 'query' field, e.g. "
                   '{"query": "vintage graphic tee under $30"}')
        record["outcome"] = "bad_request"
        record["error"] = message
        return jsonify({"error": message}), 400

    wardrobe = payload.get("wardrobe")
    record["wardrobe"] = "custom" if isinstance(wardrobe, dict) else "example"
    if not isinstance(wardrobe, dict):
        wardrobe = get_example_wardrobe()

    # A queued request should look like a queued request. Without this the
    # second caller just sits there, and "slow" and "waiting its turn" are
    # indistinguishable from the outside — which is how people conclude the
    # deployment is broken when it is behaving exactly as designed.
    #
    # This is NOT the logging you add in the follow-along. It prints nothing
    # on the normal path, carries no timing and counts nothing; it says only
    # that this request had to wait. `locked()` can be a moment out of date,
    # so the note is occasionally missed — which costs nothing, because
    # nothing depends on it.
    if _one_at_a_time.locked():
        print(
            "  [serve] another request is still running. This one is waiting "
            "its turn — serve.py handles one at a time, on purpose.",
            file=sys.stderr,
            flush=True,
        )

    failure = None
    session = None
    queued_from = time.perf_counter()
    with _one_at_a_time:
        record["queued_ms"] = round((time.perf_counter() - queued_from) * 1000, 1)
        # Inside the lock nothing else calls the model, so the before/after
        # difference in generate's counters is exactly this request's spend.
        calls_before = generate.call_count()
        hits_before = generate.cache_hits()
        tokens_before = generate.token_counts()
        agent_start = time.perf_counter()
        try:
            session = run_agent(query, wardrobe)
        except Exception as exc:  # noqa: BLE001 — a 500 with a sentence beats a hang
            failure = f"{type(exc).__name__}: {exc}"
        record["agent_ms"] = round((time.perf_counter() - agent_start) * 1000, 1)
        tokens_after = generate.token_counts()
        record["model_calls"] = generate.call_count() - calls_before
        record["cache_hits"] = generate.cache_hits() - hits_before
        record["tokens_prompt"] = tokens_after["prompt"] - tokens_before["prompt"]
        record["tokens_output"] = tokens_after["output"] - tokens_before["output"]
        record["tokens_total"] = tokens_after["total"] - tokens_before["total"]

    # Outside the lock: building a response is not work the next caller should
    # be waiting on.
    if failure is not None:
        record["outcome"] = "server_error"
        record["error"] = failure
        return jsonify({"error": failure}), 500

    record["outcome"] = session.get("outcome")
    record["error"] = session.get("error")
    record["timings"] = session.get("timings")
    if session.get("selected_item"):
        record["selected_item"] = session["selected_item"].get("id")
    if session.get("fit_card"):
        record["fit_card_chars"] = len(session["fit_card"])
    return jsonify(session), 200


if __name__ == "__main__":
    # PORT and 0.0.0.0 are not decoration. A host tells you which port to
    # listen on through PORT, and it reaches your process from outside the
    # container — bind 127.0.0.1 and nothing but the container itself can
    # connect, which looks exactly like a broken app from the browser.
    port = int(os.getenv("PORT", "5000"))

    # Never on by default. Flask's debugger executes code typed into a browser,
    # and a deployed app with it on is a stranger's shell. Set AI201_DEBUG=1 in
    # your own terminal when you want the reloader.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"\nFitFindr is listening on http://localhost:{port}")
    print("It runs one request at a time — a second one waits for the first.")
    print("Ask it something (single quotes, as always):\n")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"query\": \"vintage graphic tee under $30\"}}'\n"
    )
    print("Ctrl-C to stop.\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
