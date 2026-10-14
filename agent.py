"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from mcp_client import MCPError, call_tool
from tools import suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── query parsing ─────────────────────────────────────────────────────────────

# "under $30", "below 30", "$30", "max $29.99"
_PRICE = re.compile(r"(?:under|below|less than|max|up to)?\s*\$\s*(\d+(?:\.\d+)?)"
                    r"|(?:under|below|less than|max|up to)\s+(\d+(?:\.\d+)?)",
                    re.IGNORECASE)
# "size M", "in size 8", "size XXS", "size W30"
_SIZE = re.compile(r"(?:in\s+)?size\s+([A-Za-z]*\d+(?:\.\d+)?|[XSML]{1,4}(?:/[XSML]{1,4})?)\b",
                   re.IGNORECASE)
# Words that say nothing about the item itself.
_FILLER = {
    "i", "im", "i'm", "a", "an", "the", "some", "something", "for", "me", "my",
    "looking", "want", "need", "find", "show", "get", "please", "in", "with",
    "and", "or", "under", "below", "max", "up", "to", "less", "than", "size",
}


def parse_query(query: str) -> dict:
    """
    Pull a description, a size and a max_price out of a plain-language query.

    Regex, no model call. Returns {"description": str, "size": str | None,
    "max_price": float | None}. `description` is "" when the query names no
    item — that's what the second branch in run_agent() checks.
    """
    max_price = None
    price = _PRICE.search(query)
    if price:
        max_price = float(price.group(1) or price.group(2))
        query = query[:price.start()] + " " + query[price.end():]

    size = None
    size_match = _SIZE.search(query)
    if size_match:
        size = size_match.group(1).upper()
        query = query[:size_match.start()] + " " + query[size_match.end():]

    words = re.findall(r"[a-z0-9']+", query.lower())
    description = " ".join(w for w in words if w not in _FILLER)

    return {"description": description, "size": size, "max_price": max_price}


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)

    session["parsed"] = parse_query(query)
    trace.step("parse_query", inputs=query, returned=str(session["parsed"]))

    # SECOND BRANCH (stretch): the query names no item, so there is nothing to
    # search for. Stop before any tool is called.
    if not session["parsed"]["description"]:
        constraints = []
        if session["parsed"]["size"]:
            constraints.append(f"size {session['parsed']['size']}")
        if session["parsed"]["max_price"] is not None:
            constraints.append(f"under ${session['parsed']['max_price']:g}")
        kept = f" I kept {' and '.join(constraints)}." if constraints else ""
        session["error"] = (
            "Your search doesn't say what kind of item you want, so there was "
            "nothing to search for." + kept + " Add an item and try again — "
            "e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'."
        )
        trace.step("branch", note="no item named in the query — stopping before search_listings")
        return session

    steps = 0

    # Step 1 — search. Inputs come out of the session, results go back in.
    steps += 1
    trace.check_iterations(steps)
    parsed = session["parsed"]
    search_inputs = {
        "description": parsed["description"],
        "size": parsed["size"],
        "max_price": parsed["max_price"],
    }
    # search_listings runs on the MCP server (mcp_server.py), not in-process.
    try:
        session["search_results"] = call_tool("search_listings", search_inputs)
    except MCPError as exc:
        session["error"] = (
            "The listings search couldn't be reached, so nothing was searched. "
            "Try the same query again in a moment; if it keeps failing, run "
            "`python mcp_server.py` on its own to see why the server won't start."
        )
        trace.step("search_listings (via MCP)", inputs=str(search_inputs),
                   returned=f"MCPError: {str(exc).splitlines()[0]}", note="stopping")
        return session
    trace.step("search_listings (via MCP)", inputs=str(search_inputs),
               returned=session["search_results"])

    # THE BRANCH: nothing matched, so stop before suggest_outfit.
    if not session["search_results"]:
        session["error"] = _no_results_message(parsed)
        trace.step("branch", note="search returned [] — stopping before suggest_outfit")
        return session

    session["selected_item"] = session["search_results"][0]
    trace.step("select item", inputs="search_results[0]",
               returned=session["selected_item"],
               note=f"id {session['selected_item']['id']} stored in session['selected_item']")

    # Steps 2 and 3 call the model. If it can't be reached, say so and keep
    # what the search found, instead of letting the exception surface.
    try:
        # Step 2 — outfit, built from the item stored in the session.
        steps += 1
        trace.check_iterations(steps)
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], session["wardrobe"]
        )
        trace.step("suggest_outfit",
                   inputs=f"new_item={session['selected_item']['id']}, "
                          f"wardrobe={len(session['wardrobe'].get('items') or [])} items",
                   returned=session["outfit_suggestion"])

        # Step 3 — fit card, from the outfit and item stored in the session.
        steps += 1
        trace.check_iterations(steps)
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
        trace.step("create_fit_card",
                   inputs=f"new_item={session['selected_item']['id']}, "
                          f"outfit={session['outfit_suggestion']}",
                   returned=session["fit_card"])
    except ModelUnavailable as exc:
        failed = "suggest_outfit" if session["outfit_suggestion"] is None else "create_fit_card"
        item = session["selected_item"]
        session["error"] = (
            f"The search worked — it found {item['title']} (${item['price']:g} on "
            f"{item['platform']}) — but the styling model couldn't be reached, so "
            f"there's no outfit or fit card. {exc} Then run the same query again."
        )
        trace.step(failed, returned=f"ModelUnavailable: {exc}", note="stopping")

    return session


def _no_results_message(parsed: dict) -> str:
    """Say what was searched and which constraint to loosen first."""
    searched = f"'{parsed['description']}'"
    if parsed["size"]:
        searched += f" in size {parsed['size']}"
    if parsed["max_price"] is not None:
        searched += f" under ${parsed['max_price']:g}"

    tips = []
    if parsed["max_price"] is not None:
        tips.append("raise or drop the price limit")
    if parsed["size"]:
        tips.append("drop the size")
    tips.append("use fewer or broader words (e.g. 'dress' instead of 'designer ballgown')")
    return f"Nothing matched {searched}. Try: " + "; ".join(tips) + "."


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
