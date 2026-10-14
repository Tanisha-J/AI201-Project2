# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr takes a plain-language thrift request like `'vintage graphic tee under $30'`
or `'90s track jacket in size M'`. It searches 40 secondhand listings
(Depop, Poshmark, thredUp…) for the best match on keywords, size and price. Then
it suggests one or two outfits that pair the find with clothes the user already
owns, and writes a short social-media caption (a "fit card") naming the item,
its price and its platform. If nothing matches, or the request doesn't name an
item at all, it stops early and says what to change instead of guessing.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Filters `data/listings.json` by price and size, then ranks what's left by keyword overlap with the description (title words ×3, style tags/colors/category ×2, description text ×1); no model call.
- **Inputs:** `description` (str), `size` (str or None — whole-token, case-insensitive match: `"M"` matches `M`, `S/M`, `M/L` but not `XL`; `"8"` matches `US 8` but not `US 8.5`; "One Size" listings match any size), `max_price` (float or None — inclusive).
- **Returns:** a `list[dict]` of at most 10 listing dicts, highest score first (cheaper first on a tie). Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), `platform`.
- **When it has nothing:** an empty list `[]` — never `None`, never an exception. Also `[]` if `description` has no words in it.

### `suggest_outfit`

- **What it does:** Asks the model for one or two outfits built around the new item, using the user's saved wardrobe when there is one.
- **Inputs:** `new_item` (dict — one listing dict from `search_listings`), `wardrobe` (dict with an `"items"` key holding a list of wardrobe-item dicts: `id`, `name`, `category`, `colors`, `style_tags`, `notes`).
- **Returns:** a non-empty `str` of plain-text outfit suggestions, under ~120 words, naming owned pieces exactly as they appear in the wardrobe.
- **When it has nothing:** if `wardrobe["items"]` is empty, it still returns a non-empty `str` — general styling advice naming generic pieces ("straight-leg jeans", "white low-top sneakers") instead of owned ones. It does not raise or return `""`.

### `create_fit_card`

- **What it does:** Asks the model for a 2–4 sentence casual caption about the find, mentioning the item, its price and its platform once each.
- **Inputs:** `outfit` (str — the string `suggest_outfit` returned), `new_item` (dict — the same listing dict).
- **Returns:** a `str` caption of 2–4 sentences. Temperature is 0.9, so the same input gives different wording each time.
- **When it has nothing:** if `outfit` is empty or only whitespace, it returns the string `"Can't write a fit card without an outfit — suggest_outfit returned nothing."` without calling the model.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in
`session["error"]` naming what was searched and what to loosen (price, size,
wording), and stop — `suggest_outfit` is never called. Otherwise, take the first
result as `session["selected_item"]` and go to `suggest_outfit`, then
`create_fit_card`.

(Second branch, before this one — see **Stretch Feature** below: if the parsed
query has no description words, stop before `search_listings` is called.)

**Where it lives:** `agent.py::run_agent` (the no-results message is built by
`agent.py::_no_results_message`)

**How the query is parsed:** regex, in `agent.py::parse_query`. A price pattern
(`under $30`, `$30`, `below 30`) becomes `max_price`, a size pattern (`size M`,
`in size 8`, `size W30`) becomes `size`, and the leftover words minus filler
(`looking`, `for`, `a`, `something`…) become `description`.

**What moves through the session:** `query` → `parsed` (description, size,
max_price) → `search_results` (list of listing dicts) → `selected_item`
(`search_results[0]`) → `outfit_suggestion` (read from `selected_item` +
`wardrobe`) → `fit_card` (read from `outfit_suggestion` + `selected_item`). Each
tool reads its inputs out of the session, not from the previous call's return
value. `error` is set only when the run stops early, and then every field after
the stopping point stays `None` / `[]`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Outfit 1: Effortless Grunge
Wear the graphic tee tucked slightly into your baggy straight-leg jeans, dark wash. Layer the vintage black denim jacket on top and finish with black combat boots and the black crossbody bag for an easy, everyday look.

Outfit 2: Streetwear Contrast
Pair the graphic tee with your wide-leg khaki trousers to play with proportions and add some contrast to the black shirt. Accessorize with the brown leather belt and chunky white sneakers to keep the outfit grounded, modern, and comfortable.

  Fit card: Score this 2003 tour bootleg tee on depop for just $24 and I am never taking it off. It has the absolute best faded grunge vibe. Can not wait to style this with baggy denim and chunky boots all fall.

0 model calls this session, 2 served from cache
```

The empty-search branch, for comparison — no model calls, stops before `suggest_outfit`:

```
$ python app.py ask 'designer ballgown size XXS under $5'

  Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').

0 model calls this session
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

$ python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
[]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Outfit 1: Casual Streetwear
Pair the vintage Levi's 501s with the white ribbed tank top tucked in. Layer the vintage black denim jacket on top and finish with chunky white sneakers and the black crossbody bag. Add the brown leather belt to break up the waistline.

Outfit 2: Cozy Classic
Wear the vintage Levi's 501s with the oversized grey crewneck sweatshirt worn slightly slouchy or half-tucked. Slip into the black combat boots and use the black crossbody bag for an effortless everyday look that plays up the classic denim texture.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Found the holy grail on depop today. These vintage Levi's 501s were only $38 and they fit like an absolute dream. Paired them with crisp white sneakers for that effortlessly cool streetwear vibe.

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('   ', load_listings()[0]))"
Can't write a fit card without an outfit — suggest_outfit returned nothing.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- i needed to put my API key in the .env file
- i put it in the wrong file
- it put it in an untracked file so it is not leaked and told me the issue

**Moment 2**

- i asked for help with framing the criterion
- it gave me ideas with a sentence frame
- i changed the wording

**Unit 4**

- I asked Claude (Claude Code) to do the unit 4 milestones in my repo and commit
  each one: the MCP move, the failure handlers, the trace, the scenarios, both
  eval runs and the write-up.
- **Moment 3 — the key.** When the model call failed with `401 UNAUTHENTICATED`,
  Claude said my key looked like an OAuth token rather than an API key because
  it didn't start with `AIza`. That was wrong — the next `test.py` run passed
  with a key in that same `AQ.` format. What I take from it: the format guess wasn't evidence; the passing
  `test.py` line was.
- **Moment 4 — the scorer.** Claude wrote a script to mark each try PASS/FAIL
  from the run log. Its first pass said criteria 2 and 3 failed 25 of 25 —
  because the branch note "stopping before suggest_outfit" contains the
  string `suggest_outfit`, and the first-result check read the wrong field.
  Reading the raw output showed both passing, and the script was fixed before
  any verdict was written. A scorer is code too, and needs checking against
  the output it scores.
- **Moment 5 — the improvement.** After the fix made criterion 5 pass 25/25,
  Claude tried five no-item phrasings the test never used; none hit the
  branch. That went into the README instead of letting the 5/5 stand on its
  own, since the fix was chosen by looking at the test's own queries.

---

## Stretch Feature — A Second Branch

**Declared before building.** This section was committed before any code for
the branch existed.

**The condition:** after the query is parsed, the size and price are taken out
of it. If no description words are left (e.g. `'under $30 size M'`), the user
never said *what* they want, so there is nothing to search for.

**The rule:** If the parsed description is empty, put a message in
`session["error"]` asking what kind of item they're looking for and stop
*before* calling `search_listings`. Otherwise, continue to `search_listings`
as normal.

**How it differs from the empty-search branch:** the empty-search branch stops
*after* `search_listings` returns `[]`. This one stops *before* any tool is
called, so `session["search_results"]` stays `[]` and `session["selected_item"]`,
`session["outfit_suggestion"]` and `session["fit_card"]` all stay `None`.

**Where it lives:** `agent.py::run_agent`

**What it changed:** `agent.py` gained `parse_query()`, a regex parser that
pulls `max_price` ("under $30") and `size` ("size M") out of the query and
drops filler words ("looking for", "something", "a"…). Whatever is left is
`session["parsed"]["description"]`. `run_agent()` now checks that description
right after parsing: if it's empty, the run stops with a message that names
what was kept (size, price) and what to add (an item, with examples). The loop
now has three possible endings instead of two: stop before search, stop after
an empty search, or run all three tools.

**Run log where the branch was taken:**

```
$ python app.py ask 'under $30 size M'

  Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size M and under $30. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.

0 model calls this session

$ python app.py ask 'looking for something under $20'

  Your search doesn't say what kind of item you want, so there was nothing to search for. I kept under $20. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.

0 model calls this session
```

Session after `run_agent('under $30 size M', get_example_wardrobe())` — no
tool ran, so nothing past `parsed` was filled in:

```
parsed: {'description': '', 'size': 'M', 'max_price': 30.0}
search_results: []
selected_item: None
outfit_suggestion: None
fit_card: None
```

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

Full output: [`results/run_2026-10-13_2242_before.md`](results/run_2026-10-13_2242_before.md),
produced by `run_eval.py::main` with caching off, temperature 0.9.

**What a "try" is.** Criteria 1 and 2 name one query, so Try *k* is the *k*-th
run of that query. Criteria 3, 4 and 5 are written as "run each of five queries
once", so Try *k* is query *k* (in the order `criteria.md` and
`app.py examples` list them), scored from its first run. `run_eval.py` ran each
of those queries five times anyway; the repeat count is in the last column so
the verdict isn't resting on one lucky round.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item = first search result, and the fit card names its title and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) — 25/25 across all repeats |
| 4. Fit card has the right price as `$N` | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) — 24/25 across all repeats |
| 5. No-item query stops before `search_listings` | 4 of 5 | PASS | PASS | PASS | FAIL | FAIL | MISSED (3/5) — 15/25 across all repeats |

**Real output from one try per criterion** (all from `agent.py::run_agent`; the
fit cards come from `tools.py::create_fit_card`, the stop messages from
`agent.py::_no_results_message` and the no-item branch in `run_agent`):

Criterion 1 — `vintage graphic tee under $30`, try 2, fit card:

```
scored this 2003 tour bootleg tee on depop for just $24 and it's officially my new uniform. obsessed with how easy it is to dress up with khakis or keep totally chill with baggy denim. the ultimate grunge streetwear piece.
```

Criterion 2 — `designer ballgown size XXS under $5`, try 1:

```
- stopped early: yes — Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').
- selected_item: (none)
- search_results: 0

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search returned [] — stopping before suggest_outfit
```

Criterion 3 — `90s track jacket in size M`, try 1. The first search result,
the selected item and the fit card are all the same jacket (`lst_004`):

```
[2] search_listings (via MCP)
      out: 5 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +2 more
[3] select item
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      →    id lst_004 stored in session['selected_item']

Fit card:
Found this vintage Champion 90s track jacket on Poshmark for just $45 and I'm obsessed. The navy and white stripes give off the ultimate retro-athletic streetwear vibe. Already planning to wear it with baggy jeans and wide-leg trousers on repeat.
```

Criterion 4 — `denim jacket under $50`, try 1 (price is $42), fit card:

```
Score! Snagged this cropped vintage Wrangler denim jacket on Poshmark for just $42 and I am obsessed. The light wash gives it such a good streetwear vibe. Can't decide if I want to style it with wide-leg trousers or go full double-denim today!
```

…and the one card out of 25 that missed — `silk slip dress in midi length under $40`, repeat 3 (price is $30):

```
Obsessed with this 90s floral silk slip dress I just scored on depop for only thirty bucks. It’s giving total grunge romance when I layer it with a chunky crewneck and combat boots. Such a versatile vintage find!
```

Criterion 5 — the two failing queries. `anything in size S` (try 4) ran every tool:

```
[1] parse_query
      in:  anything in size S
      out: {'description': 'anything', 'size': 'S', 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': 'anything', 'size': 'S', 'max_price': None}
      out: 1 items: Knit Cardigan — Chunky Brown
[3] select item
      out: Knit Cardigan — Chunky Brown ($35.0, depop)
      →    id lst_008 stored in session['selected_item']
[4] suggest_outfit
[5] create_fit_card
      out: Finally scored this chunky brown knit cardigan on depop for just $35 and I am never taking it off. …
```

`cheap stuff under $10` (try 5) stopped, but at the wrong branch and with the wrong message:

```
- stopped early: yes — Nothing matched 'cheap stuff' under $10. Try: raise or drop the price limit; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').
- search_results: 0

[1] parse_query
      out: {'description': 'cheap stuff', 'size': None, 'max_price': 10.0}
[2] search_listings (via MCP)
      out: [] (empty)
[3] branch
      →    search returned [] — stopping before suggest_outfit
```

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | **MET** (5/5) | All five runs of `vintage graphic tee under $30` reached `create_fit_card` and returned a non-empty card; no run stopped or crashed. |
| 2 | Impossible query stops before `suggest_outfit` | 5 of 5 | **MET** (5/5) | All five runs stopped with the "Nothing matched … Try:" message, and no trace has a `suggest_outfit` step. 0 model calls. |
| 3 | Selected item = first result, card names it | 5 of 5 | **MET** (5/5) | For each of the five queries, the id in `selected_item` matched the first search result, and the card contained title words and the platform. Held in 25/25 runs, not just the five scored. |
| 4 | Fit card has the right price as `$N` | 4 of 5 | **MET** (5/5) | All five scored cards had `$` + the item's price. Across all 25 cards, one wrote "thirty bucks"; no round of five dropped below 4, so the target held every time, not just once. |
| 5 | No-item query stops before search | 4 of 5 | **MISSED** (3/5) | 3 of the 5 queries took the no-item branch. Two didn't — and because the parser is deterministic, they failed on all five repeats, so this isn't bad luck. |

**Diagnoses**

**Criterion 5 — missed 2 of 5. Where: the loop's branch** (`agent.py::parse_query`,
which feeds the no-item check in `run_agent`). **Mechanism:** the branch decides a
query names no item when nothing is left after stripping filler words, and the
filler list is hand-written. "anything", "stuff" and "cheap" aren't on it.

- `anything in size S` → description `'anything'`. The branch let it through, and
  `search_listings` did its job correctly: the Knit Cardigan's description ends
  "Perfect for layering over **anything**", so it scored 1. The run then called
  the model twice and produced an outfit and fit card for a cardigan the user
  never asked for. Nothing errors, so from the outside this looks like a search
  bug — it isn't; the search was given a word it should never have received.
- `cheap stuff under $10` → description `'cheap stuff'`. Search found nothing,
  so the *empty-search* branch caught it. The run stopped, but the message tells
  the user to "use fewer or broader words" — wrong advice when the real problem
  is that they never said what they want.

**Pattern:** both misses are the same problem, not two. Every tool behaved to
spec in every run; the only failure in 65 runs is a word list that's one step
upstream of all three tools. It's exactly the risk I named in `criteria.md`
when I set the target at 4 rather than 5 — I just underestimated how many
everyday phrasings it would miss.

**Criterion 4's one non-pass (not a miss of the target):** `create_fit_card`'s prompt
asks for the price as `$30`, but at temperature 0.9 the model occasionally
writes it out casually ("thirty bucks"). Same failure I saw in unit 3. It's
model output, not the tool or the session, and at 1 in 25 it stays inside the
4-of-5 target.

**Were my targets too low?** Criterion 1 is: I set 4 of 5 to allow for keyword
misses and rate-limit failures, and got 5/5 with three rate-limit waits along
the way — the pacing in `generate.py` absorbs them. For the query this
criterion names, 5 of 5 is the honest target. I'm leaving the original number
in place because tightening a target after meeting it isn't what a revision
is for, but it's the one I'd raise next time.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path** — five steps; step 2 is the MCP call.

```
$ python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Vintage Graphic Hoodie — Faded Black … +7 more
[3] select item
      in:  search_results[0]
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      →    id lst_006 stored in session['selected_item']
[4] suggest_outfit
      in:  new_item=lst_006, wardrobe=10 items
      out: Outfit One: Grunge Street Wear the 2003 Tour Bootleg Style graphic tee with the baggy straight-leg jeans and b…
[5] create_fit_card
      in:  new_item=lst_006, outfit=Outfit One: Grunge Street Wear the 2003 Tour Bootleg Style graphic tee with the baggy…
      out: scored this 2003 tour bootleg style graphic tee on depop for just $24 and it's officially my new uniform. goin…

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Outfit One: Grunge Street
Wear the 2003 Tour Bootleg Style graphic tee with the baggy straight-leg jeans and black combat boots. Layer the vintage black denim jacket on top and add the black crossbody bag for an effortless, edgy look. 

Outfit Two: Contrast Casual
Pair the graphic tee with the wide-leg khaki trousers and the chunky white sneakers. Cinch the waist using the brown leather belt and throw on the black cropped zip hoodie to wear open or tied around your shoulders for a balanced, modern everyday style.

  Fit card: scored this 2003 tour bootleg style graphic tee on depop for just $24 and it's officially my new uniform. going for total grunge street energy today with baggy denim and beat-up combat boots. honestly obsessed with how effortlessly edgy it looks.

2 model calls this session, 480 prompt + 166 output tokens
```

**Empty search** — stops at step 3, before any model call.

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
[3] branch
      →    search returned [] — stopping before suggest_outfit

  Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').

0 model calls this session
```

**On the MCP move:** `search_listings` is now registered on the FastMCP server
in `mcp_server.py`. Its docstring is the published description: units
(`max_price` in US dollars, inclusive), the whole-size matching rule, every
returned field, and the empty case (`[]`, never null or an error).
`python mcp_client.py` lists it with `description: string`, `size: string
(optional)`, `max_price: number (optional)` — the same types as the Tool
Inventory. In `agent.py::run_agent` the direct call became
`call_tool("search_listings", {...})`; nothing else in the loop changed.
**Nothing behaved differently:** for `vintage graphic tee` / `None` / `30.0` the
MCP result and the direct call were `==` (same 10 dicts, same order), and the
impossible query still came back as `[]`, so the empty-search branch fires
exactly as before. The one visible cost is speed — `mcp_client.call_tool`
starts the server for each call. I also added a handler for `MCPError`, so a
server that won't start gives the user a message instead of a traceback.

**Failure modes, triggered on purpose** (what the agent said each time):

| Failure | How I triggered it | What the agent said |
|---|---|---|
| Empty search | `python app.py ask 'designer ballgown size XXS under $5'` | `Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').` |
| Empty wardrobe | `python app.py ask 'denim jacket under $50' --empty-wardrobe` | No crash, no empty string — general advice: `Outfit one: Lean into a casual streetwear vibe. Pair the cropped Wrangler jacket with high-waisted black wide-leg trousers and a fitted ribbed white tank top. Finish with chunky retro sneakers and a simple canvas tote bag…` (the handling already existed in `tools.py::suggest_outfit`; 5/5 in both eval runs) |
| Model unavailable | A wrong key, on a query I hadn't run before: `GEMINI_API_KEY=AIza…(fake) python app.py ask 'leather bomber jacket under $70'` | `The search worked — it found Leather Belt — Brown, Braided ($12 on thredUp) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.` |

Before the handler, the model-unavailable case ended the run with the bare
exception line `ModelUnavailable: The model rejected your API key…` and threw
away the search result. Now `run_agent` catches `ModelUnavailable` around
steps 2–3, keeps what search found, and says what to do.

---

## The Improvement

**What I changed:** one edit to `agent.py` — nine words added to `_FILLER`,
the list `parse_query` strips before deciding whether the query names an item:
`anything`, `everything`, `whatever`, `stuff`, `thing`, `things`, `item`,
`items`, `cheap`. Nothing else changed between the two runs (commit `f7e03ef`).

**Which failure it was meant to fix:** criterion 5. The diagnosis put both
misses on the filler list: `anything` reached `search_listings` and matched a
cardigan's description text, and `cheap stuff` fell through to the
empty-search branch with the wrong advice. A tool fix or a prompt rewrite
wouldn't have touched either — every tool did what it was asked.

### Run Log — After

Full output: [`results/run_2026-10-13_2249_after.md`](results/run_2026-10-13_2249_after.md).
Same scenarios, same five tries, caching off. Before is repeated here so the
two sit side by side.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item = first result, card names it | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) — 25/25 across all repeats |
| 4. Fit card has the right price as `$N` | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) — 25/25 across all repeats |
| 5. No-item query stops before `search_listings` | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) — 25/25 across all repeats |

| Criterion | Before | After |
|---|---|---|
| 1 | MET 5/5 | MET 5/5 |
| 2 | MET 5/5 | MET 5/5 |
| 3 | MET 5/5 (25/25) | MET 5/5 (25/25) |
| 4 | MET 5/5 (24/25) | MET 5/5 (25/25) |
| 5 | **MISSED 3/5 (15/25)** | **MET 5/5 (25/25)** |
| Model calls for the whole run | 80 | 70 |

Criterion 5 after — the two queries that failed before (`agent.py::run_agent`,
first try of each):

```
- stopped early: yes — Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size S. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.
- search_results: 0

[1] parse_query
      in:  anything in size S
      out: {'description': '', 'size': 'S', 'max_price': None}
[2] branch
      →    no item named in the query — stopping before search_listings
```

```
- stopped early: yes — Your search doesn't say what kind of item you want, so there was nothing to search for. I kept under $10. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.
- search_results: 0

[1] parse_query
      in:  cheap stuff under $10
      out: {'description': '', 'size': None, 'max_price': 10.0}
[2] branch
      →    no item named in the query — stopping before search_listings
```

**Did it help, and how do I know:** yes, on what the test measures — criterion 5
went from 3/5 to 5/5, both failing queries now stop at step 2 with the right
message, and the run made 10 fewer model calls because `anything in size S` no
longer styles a cardigan nobody asked for. No other row moved: criteria 1–3
were unchanged and criterion 4's 24/25 → 25/25 is the model's wording varying,
not the fix (the fit-card prompt didn't change).

But it helped less than the table suggests. I chose the words by looking at
the two queries that failed, and those are the same queries the test runs, so
the after-score is partly the fix being graded on its own answer key. I
checked five no-item phrasings the test never used:

```
'something cute in size M'      -> 'cute'                  | ran all tools on Y2K Baby Tee — Butterfly Print
'any clothes under $25'         -> 'any clothes'           | empty-search branch
'what do you have in size L'    -> 'what do you have'      | empty-search branch
'show me deals under $15'       -> 'deals'                 | empty-search branch
'nothing too expensive, size S' -> 'nothing too expensive' | empty-search branch
```

0 of 5 reached the no-item branch. The criterion is met; the mechanism behind
it — a hand-written word list — is not fixed.

---

## What's Still Broken

Every criterion is met after the change, so nothing here is a missed target —
but three things are broken that the criteria don't catch.

**1. The no-item branch still depends on a word list (criterion 5's real cause).**
Unseen phrasings miss it 5 of 5 times (see above). What I'd do: flip the check
around — instead of listing words that *aren't* items, require at least one
word that *is* one (a category or garment word from the listings' `category`,
`title` and `style_tags`, plus a short list of common garment nouns), and send
anything else to the no-item message. I stopped because that is a second
change to the same branch, and this unit allows one; it also needs care so
`designer ballgown` — a real item the data doesn't have — still reaches the
empty-search branch and criterion 2 doesn't break. I'd also rewrite
criterion 5's five queries with phrasings I hadn't tuned against.

**2. Search picks a weak match without saying the strong one was just over budget.**
`'leather bomber jacket under $70'` selected a $12 leather **belt**: the only
bomber is $75, so the price filter removes it, the remaining listings each
match one word, and the cheapest wins the tie. The user gets an outfit built
around a belt. What I'd do: in `run_agent`, if the top result matches fewer
than half the description words, stop with a "closest match was X at $75 —
raise the limit?" message instead of styling it. I found this while
triggering the model-unavailable failure, after the runs were done; no
criterion covers it, so I'd write one first.

**3. Fit cards occasionally spell the price out.** 1 in 25 before, 0 in 25
after, with no change to the prompt — so the after number is luck, not a fix.
Within criterion 4's target, so I left it. If it mattered, I'd check the card
in `create_fit_card` for `$<price>` and, if missing, retry once rather than
reword the prompt again.

**Criterion 1's target is too low.** 5/5 in both runs, with rate-limit waits
absorbed by `generate.py`. I'd raise it to 5 of 5 next time — but not by
editing it now, since that isn't a revision the brief allows.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
