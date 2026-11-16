# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

My search is a plain keyword match on words in the title, tags and
description, with no synonyms — a phrasing like "band shirt" won't score
against listings titled "tee", so some real matches will be missed. Both later
tools also call the model, and a rate-limit wait or a failed call can end a run
early, which 5 of 5 wouldn't allow for.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

This path never touches the model: `parse_query` is regex, `search_listings` is
pure Python over a fixed file, and `run_agent` checks `if not
session["search_results"]` before `suggest_outfit` can run. Nothing on it is
random, so a single miss means the branch is broken — not unlucky.

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

Run each of the five matching queries from `python app.py examples` once and
print the session. In 5 of 5 runs, `session["selected_item"]["id"]` equals
`session["search_results"][0]["id"]`, **and** the fit card names that same
item — at least one distinctive word from its `title` (e.g. "track jacket",
"501") and its `platform` appear in `session["fit_card"]`.

**Why this target:**

`suggest_outfit` and `create_fit_card` both read the item out of
`session["selected_item"]` instead of from each other's return values, so the id
check should never fail — if it does, the session is being overwritten. The
fit-card half catches the model describing an item it wasn't given. I kept it at
5 of 5 because the prompt hands the model the exact title and platform, so a
card about a different item would be a real bug, not wording variation.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

Run each of the five matching queries from `python app.py examples` once. In at
least 4 of the 5 fit cards, the price is written in digits after a `$` sign and
equals the selected item's `price` (`$24` and `$24.00` both count;
"twenty-four bucks" or no price at all does not).

**Why this target:**

The fit card runs at temperature 0.9 and the model writes casual captions, so
it sometimes spells prices out — in my own Milestone 4 test, one of three cards
for the same Levi's said "thirty-eight bucks" instead of "$38". The prompt does
ask for the price as `$38`, so most cards should get it right, but 5 of 5 would
ignore a failure I have already seen happen.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

Run these five queries, which name a size or price but no item: `'under $30 size
M'`, `'size W30'`, `'looking for something under $20'`, `'anything in size S'`,
`'cheap stuff under $10'`. In at least 4 of 5, the agent stops **before**
`search_listings` with the message asking what kind of item they want,
`session["search_results"]` is `[]`, and the run makes 0 model calls.

**Why this target:**

This is my stretch branch. `parse_query` decides there's "no item" by stripping
words on a hand-written filler list (`looking`, `for`, `something`…). Words
like "anything", "cheap" or "stuff" aren't on that list, so a query using them
gets sent to search as if it were a description and falls into the
empty-search branch instead — the user gets a less useful message. 4 of 5
allows for one phrasing my list doesn't cover; 5 of 5 would assume the list is
complete, and I know it isn't.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone acceptance criteria — FitFindr as a logged service

Written for the capstone (shape A, deploy and instrument), **before any trial
was run**. They are about `python serve.py` and its request log
(`logs/requests.jsonl`), not the CLI. Criteria C1, C2, C3 and C5 are about the
extension; C4 is about the HTTP layer the extension sits on.

**One trial** = one fresh server with the real key, sent this fixed set of
requests in order, with a 6 s pause after each completed run:

- 10 matching queries: the five from `python app.py examples`, twice each
- 2 impossible queries (`designer ballgown size XXS under $5`, `gold sequin gown size 2 under $3`)
- 2 no-item queries (`size W30`, `under $30 size M`)
- 5 malformed bodies: no body at all, `{}`, `{"query": ""}`, `{"query": 42}`, `["denim jacket"]`

Then a second fresh server started with `GEMINI_API_KEY=not-a-real-key`, sent
`denim jacket under $50` 5 times. That's 24 requests per trial. Each criterion
runs three trials, changing nothing in between.

---

## C1. Every request leaves exactly one complete log record

For all 24 requests in a trial, `logs/requests.jsonl` contains **exactly one**
line whose `request_id` equals the response's `X-Request-ID` header. The line
parses as JSON and has all 19 documented fields, with `status` matching the HTTP
status the client got. **Target: 24 of 24, every trial.**

**Why this target:** the log is the only way to find out later what happened.
A request with no record, or two, is a failure I can't see. Writing the line
is not random: it happens in a `finally` in `serve.py::ask`. So anything below
24 means a code path skips the `finally` or writes twice, and that's a bug, not
noise. The 500s and the bad-key requests are in the set on purpose, because
failures are the records most likely to go missing and the ones I most need.

## C2. The logged numbers match what actually happened

For each of the 10 completed runs in a trial: the logged `duration_ms` is
within **250 ms** of the client's measured time (curl's `time_total`), **and**
`model_calls` is exactly 2, **and** `tokens_total` is greater than 0.
**Target: 10 of 10, every trial.**

**Why this target:** a log that is complete but wrong is worse than none,
because I'd trust it. My cost number (657 tokens/run) and the latency stretch
both come from these fields. 250 ms, not something tighter: the client's time
also includes connecting over localhost and turning the session into JSON,
which my timer doesn't cover. That should be milliseconds, but the session holds
the 40-listing search results. Anything over 250 ms means the timer is missing
real work, for example a queue wait or response building. Exactly 2 calls,
because a completed run makes `suggest_outfit` + `create_fit_card` and nothing
else. A third call would mean a hidden retry.

## C3. A dead API key fails fast, says why, and is logged as a failure

For each of the 5 bad-key requests in a trial: the response comes back in
**under 5 seconds** (curl `time_total`). Its JSON `error` contains the words
"API key". Its log record has `outcome` = `model_unavailable` and
`tokens_total` = 0. **Target: 5 of 5, every trial.**

**Why this target:** a bad or revoked key is the most likely way this
service breaks for real, and nothing about it is visible from `/health`. The
user should find out quickly and the log should make it obvious. 5 seconds,
because in my cost measurement a successful run took a median of 2.6 s, and
failing should never take longer than succeeding by much. A rejected key needs
one MCP search (~0.3–1 s) and one refused model call. During the build I saw
a single bad-key request take 8.9 s when the MCP search started cold (5.0 s), so
I'm not certain the first request in a trial will make it. That's what this
criterion is here to find out.

## C4. Malformed requests get a 400, never a 500

Each of the 5 malformed bodies gets HTTP **400** with a JSON body that has an
`error` field saying what to send. **Target: 5 of 5, every trial.**

**Why this target:** a 400 tells the caller they can fix it; a 500 says the
server broke, which here would be a lie. Nothing about it is random, so one
miss is a bug. I'm writing this one knowing a likely miss: the build smoke test
showed `{"query": 42}` crashing with `AttributeError: 'int' object has no
attribute 'strip'`. `serve.py`'s validation came from the starter and only
checks that a query exists, not that it's a string. The target stays at 5 of 5
because a 500 is wrong for every one of them.

## C5. Warm requests come back quickly enough to wait for

Of the 10 completed runs in a trial, at least **9 have a logged `duration_ms`
of 10,000 ms or less**. Warm means the server is already running; the
5 s pause per run keeps under the rate limit, so the rate-limit wait isn't
what gets measured. **Target: 9 of 10, every trial.**

**Why this target:** people asking for an outfit idea will wait a few seconds,
not half a minute. Ten seconds is about where a spinner turns into "is it
broken?". In my cost measurement 9 of 10 runs finished under 4.4 s (one took
13.0 s). But in the latency stretch only 9 of 15 were under 10 s, and the
worst was 26 s, all of it inside the two model calls. 9 of 10 and not 10 of 10,
because the slow tail comes from the Gemini API and I can't control it. Fewer than
9 would mean a slow request is normal, not rare.
