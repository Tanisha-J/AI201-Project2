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

---

## Capstone

**What This Extends**

This extends **FitFindr**, my unit 3–4 thrift-shopping agent: a regex query parser, `search_listings` over MCP, then two model calls (`suggest_outfit`, `create_fit_card`), with branches that stop early when the query names no item or nothing matches. Until now it only ever ran as a one-shot command (`python app.py ask`) and left no record behind. What's new is the operational layer. FitFindr now runs as a long-lived HTTP service (`python serve.py`). Every request, including rejected and failed ones, writes one structured JSON record to `logs/requests.jsonl`. That record holds the outcome, per-stage timings, the number of model calls and the tokens spent. So I can now answer "what happened on that request, and what did it cost?" without adding code first.

**The Shape**

**Shape A: deploy and instrument.** The extension is the run path (`serve.py` started by one documented command), the structured request log, and the numbers that come out of it (latency per stage, tokens and model calls per run). I'm running it locally with a committed log (Path B). The model is called over an API, so nothing is too big for a host, but a run record I can commit is the evidence that counts either way.

Out of scope, on purpose:
- **No hosting (Path A).** It's worth the same, and the time is better spent on testing.
- **No fix for the no-item word list.** That's the unit 4 miss still listed in What's Still Broken above. It's agent logic, not the operational layer.
- **No long-lived MCP connection.** The latency stretch below shows ~1 s per request goes to starting `mcp_server.py`, but removing that means rewriting `mcp_client.py`, which is a second extension.
- **No changes to prompts, tools or the session.** The agent's behaviour should be identical to unit 4. Only the code around it changes.

**Running It**

**Path B, local with logs.** One command, `python serve.py`, starts FitFindr as an HTTP service on port 5050. [RUNNING.md](RUNNING.md) has the clean-checkout setup, the Python version, the pinned dependencies (`requirements-lock.txt`) and where the log goes. There are no model files. I tested it from a fresh `git clone` into an empty folder, and the setup and server worked first time. Then the documented command failed on my own Mac. AirPlay Receiver already listens on port 5000, so `python serve.py` printed "Address already in use" and every request got a 403 from AirPlay, not FitFindr. The default port is now 5050, and RUNNING.md says why.

**Instrumentation**

`serve.py` writes one JSON object per line to `logs/requests.jsonl` for **every** `/ask` request, written in a `finally` so a crash still leaves a record. Each record has:

| Field | What it holds |
|---|---|
| `ts`, `request_id` | UTC arrival time; an id also returned as the `X-Request-ID` header |
| `query`, `wardrobe` | what came in (raw, whatever its type); `example` or `custom` wardrobe |
| `status`, `outcome`, `error` | HTTP status; how the run ended (`completed`, `no_item`, `no_results`, `search_unavailable`, `model_unavailable`, `bad_request`, `server_error`); the error text the caller saw |
| `selected_item`, `fit_card_chars` | which listing the agent chose; how long the card was |
| `queued_ms`, `agent_ms`, `duration_ms` | waiting for the one-at-a-time lock; inside `run_agent()`; the whole request |
| `timings` | per-stage ms from `agent._timed()`, including `<stage>.rate_limit_wait` if `generate.py` paused |
| `model_calls`, `cache_hits`, `tokens_prompt/output/total` | spend for this request, as the Gemini API reported it (the difference in `generate.py`'s counters across the run, measured inside the lock so no other request can mix in) |

`outcome` is set by `run_agent` itself on each exit path (`agent.py`), so the log never has to guess from error text.

The 15 records below are from one session on 2026-11-15, verbatim from `logs/requests.jsonl`. There are 10 completed runs (the five matching queries, twice each), then deliberate bad paths: an impossible query (`no_results`), a no-item query (`no_item`), an empty query (`400 bad_request`), a non-string query (`500 server_error`, a real bug, see the criteria), and one request to a second server started with a fake API key (`model_unavailable`).

```jsonl
{"ts": "2026-11-16T06:40:26.989+00:00", "request_id": "e987aaf179d0", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 249, "queued_ms": 0.0, "agent_ms": 2790.8, "duration_ms": 2791.6, "timings": {"parse_query": 0.1, "search_listings_mcp": 629.1, "suggest_outfit": 1536.9, "create_fit_card": 624.2, "total": 2790.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 474, "tokens_output": 165, "tokens_total": 639}
{"ts": "2026-11-16T06:40:35.815+00:00", "request_id": "b7bfbfb82b59", "route": "/ask", "query": "vintage graphic tee under $30", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_006", "fit_card_chars": 220, "queued_ms": 0.0, "agent_ms": 4342.7, "duration_ms": 4343.7, "timings": {"parse_query": 0.0, "search_listings_mcp": 372.4, "suggest_outfit": 3117.6, "create_fit_card": 852.1, "total": 4342.6}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 471, "tokens_output": 156, "tokens_total": 627}
{"ts": "2026-11-16T06:40:46.192+00:00", "request_id": "066b0baecc41", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 209, "queued_ms": 0.0, "agent_ms": 12977.2, "duration_ms": 12978.1, "timings": {"parse_query": 0.0, "search_listings_mcp": 392.3, "suggest_outfit": 11810.0, "create_fit_card": 773.7, "total": 12977.2}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 483, "tokens_output": 150, "tokens_total": 633}
{"ts": "2026-11-16T06:41:05.208+00:00", "request_id": "b84a75ce0394", "route": "/ask", "query": "90s track jacket in size M", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_004", "fit_card_chars": 232, "queued_ms": 0.0, "agent_ms": 1912.6, "duration_ms": 1913.6, "timings": {"parse_query": 0.0, "search_listings_mcp": 412.0, "suggest_outfit": 838.5, "create_fit_card": 661.6, "total": 1912.6}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 500, "tokens_output": 173, "tokens_total": 673}
{"ts": "2026-11-16T06:41:13.155+00:00", "request_id": "e4f707139b44", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 227, "queued_ms": 0.0, "agent_ms": 2682.6, "duration_ms": 2683.5, "timings": {"parse_query": 0.0, "search_listings_mcp": 415.3, "suggest_outfit": 1271.6, "create_fit_card": 995.0, "total": 2682.6}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 524, "tokens_output": 194, "tokens_total": 718}
{"ts": "2026-11-16T06:41:21.877+00:00", "request_id": "ae863dcedce7", "route": "/ask", "query": "silk slip dress in midi length under $40", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_013", "fit_card_chars": 249, "queued_ms": 0.0, "agent_ms": 2420.5, "duration_ms": 2421.5, "timings": {"parse_query": 0.0, "search_listings_mcp": 400.9, "suggest_outfit": 1062.9, "create_fit_card": 956.2, "total": 2420.5}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 525, "tokens_output": 200, "tokens_total": 725}
{"ts": "2026-11-16T06:41:30.342+00:00", "request_id": "9cddb73b4672", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 224, "queued_ms": 0.0, "agent_ms": 2289.0, "duration_ms": 2289.9, "timings": {"parse_query": 0.0, "search_listings_mcp": 396.7, "suggest_outfit": 1021.7, "create_fit_card": 870.1, "total": 2289.0}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 461, "tokens_output": 146, "tokens_total": 607}
{"ts": "2026-11-16T06:41:38.668+00:00", "request_id": "73b3b202747a", "route": "/ask", "query": "platform sneakers size 8", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_019", "fit_card_chars": 197, "queued_ms": 0.0, "agent_ms": 2470.5, "duration_ms": 2471.3, "timings": {"parse_query": 0.0, "search_listings_mcp": 328.1, "suggest_outfit": 1201.9, "create_fit_card": 939.9, "total": 2470.5}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 480, "tokens_output": 159, "tokens_total": 639}
{"ts": "2026-11-16T06:41:47.180+00:00", "request_id": "d990ac262e73", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 266, "queued_ms": 0.0, "agent_ms": 3199.4, "duration_ms": 3200.3, "timings": {"parse_query": 0.0, "search_listings_mcp": 337.1, "suggest_outfit": 1213.1, "create_fit_card": 1648.5, "total": 3199.4}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 476, "tokens_output": 171, "tokens_total": 647}
{"ts": "2026-11-16T06:41:56.417+00:00", "request_id": "63b41d82ae0b", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "completed", "error": null, "selected_item": "lst_007", "fit_card_chars": 271, "queued_ms": 0.0, "agent_ms": 3598.8, "duration_ms": 3599.8, "timings": {"parse_query": 0.0, "search_listings_mcp": 352.7, "suggest_outfit": 1279.6, "create_fit_card": 1965.8, "total": 3598.8}, "model_calls": 2, "cache_hits": 0, "tokens_prompt": 485, "tokens_output": 177, "tokens_total": 662}
{"ts": "2026-11-16T06:42:06.057+00:00", "request_id": "586d0abb67e4", "route": "/ask", "query": "designer ballgown size XXS under $5", "wardrobe": "example", "status": 200, "outcome": "no_results", "error": "Nothing matched 'designer ballgown' in size XXS under $5. Try: raise or drop the price limit; drop the size; use fewer or broader words (e.g. 'dress' instead of 'designer ballgown').", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 339.9, "duration_ms": 340.5, "timings": {"parse_query": 0.0, "search_listings_mcp": 339.7, "total": 339.9}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:42:06.409+00:00", "request_id": "245dfad51c58", "route": "/ask", "query": "anything in size S", "wardrobe": "example", "status": 200, "outcome": "no_item", "error": "Your search doesn't say what kind of item you want, so there was nothing to search for. I kept size S. Add an item and try again — e.g. 'graphic tee', 'denim jacket' or 'platform sneakers'.", "selected_item": null, "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 0.1, "duration_ms": 0.4, "timings": {"parse_query": 0.0, "total": 0.1}, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:42:06.420+00:00", "request_id": "b740f2e3187a", "route": "/ask", "query": "", "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:42:06.429+00:00", "request_id": "27d35b01a2fd", "route": "/ask", "query": 42, "wardrobe": null, "status": 500, "outcome": "server_error", "error": "AttributeError: 'int' object has no attribute 'strip'", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:42:08.030+00:00", "request_id": "fda769cc836a", "route": "/ask", "query": "denim jacket under $50", "wardrobe": "example", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found Denim Jacket — Light Wash, Cropped ($42 on poshmark) — but the styling model couldn't be reached, so there's no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.", "selected_item": "lst_007", "fit_card_chars": null, "queued_ms": 0.0, "agent_ms": 966.2, "duration_ms": 966.7, "timings": {"parse_query": 0.1, "search_listings_mcp": 505.9, "suggest_outfit": 460.0, "total": 966.2}, "model_calls": 1, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
```

**What It Costs**

Measured: **657 tokens and 2 model calls per completed run** (mean of 10). That's about **$0.00057 a run** at paid-tier prices, and $0 on the free tier I actually use.

How I measured it: the 10 completed runs above, cache off (`serve.py` turns it off), each record's `tokens_prompt` and `tokens_output` as reported by the API in `response.usage_metadata`. That's what the run used, not an estimate.

| Per completed run (n = 10) | Mean | Min | Max |
|---|---|---|---|
| Prompt tokens | 487.9 | 461 | 525 |
| Output tokens | 169.1 | 146 | 200 |
| Total tokens | 657 | 607 | 725 |
| Model calls | 2 | 2 | 2 |
| Wall-clock seconds | 3.87 | 1.91 | 12.98 |

Converting to dollars uses Google's paid-tier price for `gemini-3.5-flash-lite`, $0.30 per 1M input and $2.50 per 1M output tokens. The token counts are measured; the price is the only number from a page.

- Per run: 487.9 × $0.30/1M + 169.1 × $2.50/1M = $0.000146 + $0.000423 = **$0.00057**
- **100 people a day, one request each:** 100 × $0.00057 = **$0.057 a day**, × 30 = **about $1.71 a month**. That's 100 × 2 = 200 model calls and 100 × 3.87 s ≈ 6.5 minutes of server time a day.

Early stops are almost free. `no_item` and `bad_request` make 0 calls. `no_results` makes 0 calls but still costs ~0.3 s for the MCP search. `model_unavailable` makes 1 failed call that reports no tokens.

One caveat: `generate.py` counts `candidates_token_count` only. If the model spends "thinking" tokens, Google bills those as output, and they wouldn't be in my count. So $0.00057 is a floor, not a ceiling.

**Run Log and Verdicts**

The criteria are in [criteria.md](criteria.md) (capstone section, committed in `32aa530` before any trial ran). Each run is one trial of the 24-request set from `capstone_trials.py`, with a fresh server per trial and nothing changed in between. Full evidence for every scored request: [results/capstone_before.md](results/capstone_before.md). Raw logs: `results/capstone_logs/before_trial{1,2,3}.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request leaves exactly one complete log record | 24 of 24 | 24/24 | 24/24 | 24/24 | **MET** |
| C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) | 10 of 10 | 10/10 | 10/10 | 9/10 | **MISSED** |
| C3. Dead key: < 5 s, says "API key", logged `model_unavailable` | 5 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| C4. Malformed requests get a 400, never a 500 | 5 of 5 | 3/5 | 3/5 | 3/5 | **MISSED** |
| C5. Warm completed runs ≤ 10,000 ms | 9 of 10 | 10/10 | 10/10 | 9/10 | **MET** |

Real output for each criterion. The scored lines come from `capstone_trials.py`'s `c1`–`c5` functions. The log lines were written by `serve.py::_write_log`, called from `serve.py::ask`.

*C1 (trial 1).* Even the crash left exactly one record, with the same id as the `X-Request-ID` header the client got:
```
{"ts": "2026-11-16T06:46:03.075+00:00", "request_id": "2e74de670c75", "route": "/ask", "query": 42, "wardrobe": null, "status": 500, "outcome": "server_error", "error": "AttributeError: 'int' object has no attribute 'strip'", "selected_item": null, "fit_card_chars": null, "queued_ms": null, "agent_ms": null, "duration_ms": 0.1, "timings": null, "model_calls": 0, "cache_hits": 0, "tokens_prompt": 0, "tokens_output": 0, "tokens_total": 0}
```

*C2 (trial 1, then the trial 3 miss):*
```
- PASS · matching · `vintage graphic tee under $30` · HTTP 200 · curl 2,844 ms · id `e4fedc810bbc` · gap 5 ms, 675 tokens
- PASS · matching · `90s track jacket in size M` · HTTP 200 · curl 2,803 ms · id `a0d8f93aa9cb` · gap 7 ms, 688 tokens
- FAIL · matching · `silk slip dress in midi length under $40` · HTTP 200 · curl 1,837 ms · id `8c5175d85051` · outcome model_unavailable; model_calls 1; tokens_total 0
```
Its log record (trial 3):
```
{"request_id": "8c5175d85051", "query": "silk slip dress in midi length under $40", "status": 200, "outcome": "model_unavailable", "error": "The search worked — it found 90s Silk Slip Dress — Floral, Midi Length ($30 on depop) — but the styling model couldn't be reached, so there's no outfit or fit card. Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} Then run the same query again.", "timings": {"parse_query": 0.0, "search_listings_mcp": 324.9, "suggest_outfit": 1507.7, "total": 1832.8}, "model_calls": 1, "tokens_total": 0, ...}
```

*C3 (trial 1):*
```
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 885 ms · id `d9209cc82c1f` · 885 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 387 ms · id `eafaec0e18e1` · 387 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 366 ms · id `6450ac056c42` · 366 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 363 ms · id `9b6e2d796554` · 363 ms
- PASS · bad_key · `denim jacket under $50` · HTTP 200 · curl 399 ms · id `f6c004664016` · 399 ms
```

*C4 (trial 1; trials 2 and 3 identical):*
```
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `338297960898` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `c62f8ef4cf8d` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `7b910a99de17` · HTTP 400
- FAIL · malformed · `{"query": 42}` · HTTP 500 · curl 2 ms · id `2e74de670c75` · HTTP 500: AttributeError: 'int' object has no attribute 'strip'
- FAIL · malformed · `["denim jacket"]` · HTTP 500 · curl 2 ms · id `00dddf27a6d4` · HTTP 500: AttributeError: 'list' object has no attribute 'get'
```

*C5:* the logged `duration_ms` of the completed runs, sorted:
```
trial 1: 2005, 2139, 2159, 2335, 2580, 2796, 2839, 3076, 3191, 5634
trial 2: 1741, 1801, 2060, 2082, 2229, 2463, 2547, 3116, 3725, 4210
trial 3: 1914, 2139, 2480, 2531, 2688, 2857, 3503, 4414, 5514   (+ the silk slip dress run that didn't complete)
```

**Diagnoses**

**C4, missed 3/5 in every trial. Stage: request validation in `serve.py::ask`, before the agent runs. Mechanism:** the starter's check was `(payload.get("query") or "").strip()`. It assumes the body is a JSON *object* and `query` is a *string*, and it only tests that the query is non-empty. `{"query": 42}` reaches `.strip()` on an int, so it raises `AttributeError`. `["denim jacket"]` is valid JSON, so `get_json` returns a list, and `.get()` raises on a list. Both escape as 500s for what is the caller's mistake. The three passes are exactly the inputs where `or {}` / `or ""` saves it (no body, `{}`, empty string). It's deterministic, so it failed identically in all three trials. I expected this one from the build smoke test.

**C2, missed in trial 3 (9/10). Stage: the model call's error handling in `generate.py::generate`, not the log. Mechanism:** Gemini answered `suggest_outfit` with **503 UNAVAILABLE ("experiencing high demand… usually temporary")**. `generate()` only retries errors that look like a rate limit (`429`, "resource exhausted", "rate limit"). Anything else raises `ModelUnavailable` on the first attempt. So a temporary overload was treated like a dead key: the run stopped after one call and the user was told the model "couldn't be reached". The log was right about all of it: 1 call, 0 tokens, `outcome: model_unavailable`, and the full 503 text. In the other 29 completed runs the logged time was within 4–7 ms of curl's, so the numbers themselves were accurate every time.

**Pattern:** C2 and C4 are different stages, but they share a cause: an error type the code didn't expect gets the wrong treatment. In `serve.py`, an unexpected input *type* becomes a 500. In `generate.py`, an unexpected *temporary* error becomes a permanent failure. In both cases the log made the miss easy to diagnose, which is what the extension was for.

**What was met, and whether the targets were too low.** C1 and C3 held in every trial, and C3 by a long way: bad-key requests took 363–885 ms against a 5,000 ms target. The 8.9 s cold start I worried about never happened again in 15 bad-key requests. The worst was the first request to each new server (~0.9 s), which fits a cold MCP process start, not a slow model. **C5 looks set too low, with one caveat.** The slowest of 29 completed runs was 5.6 s, nowhere near 10 s. But the latency stretch, run only ~15 minutes earlier, had 7 of 15 runs over 10 s and a 26 s worst case. So the API's speed swings a lot over short periods, and three trials in a quiet stretch don't show C5 is safe. I'd still tighten it to *9 of 10 under 6,000 ms*, which is what this service delivers when the API is healthy, and expect it to miss when the API is having a bad stretch. That's the moment I'd want the criterion to catch. I'd tighten C3 to *under 2,000 ms*. C2's ±250 ms was also loose, since every gap was 4–7 ms.

**The Improvement**

**What I changed:** request validation in `serve.py::_ask` (commit `acca64e`), aimed at the C4 diagnosis. It now checks the *types* before touching the body. A body that isn't a JSON object is treated as `{}`. A `query` that isn't a string is treated as empty and rejected with a 400 that names the problem (`'query' must be text, not int.`). Nothing else changed: no prompt, tool, agent or logging code. I picked this over the C2 miss because its mechanism was fully explained and it failed every trial, so a re-run could show whether the fix worked. The 503 hit once in 30 runs, so three re-runs would most likely never trigger it, and I'd have nothing to measure a retry fix against.

**After the change**: same 24-request set, three new trials, nothing else touched. Evidence: [results/capstone_after.md](results/capstone_after.md); raw logs `results/capstone_logs/after_trial{1,2,3}.jsonl`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Every request leaves exactly one complete log record | 24 of 24 | 24/24 | 24/24 | 24/24 | **MET** |
| C2. Logged numbers match (±250 ms, 2 calls, tokens > 0) | 10 of 10 | 10/10 | 10/10 | 10/10 | **MET** |
| C3. Dead key: < 5 s, says "API key", logged `model_unavailable` | 5 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| C4. Malformed requests get a 400, never a 500 | 5 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| C5. Warm completed runs ≤ 10,000 ms | 9 of 10 | 10/10 | 9/10 | 9/10 | **MET** |

Side by side:

| Criterion | Before (runs 1/2/3) | After (runs 1/2/3) | What changed it |
|---|---|---|---|
| C1 | 24/24/24 | 24/24/24 | nothing |
| C2 | 10/10/**9** | 10/10/10 | **luck, not the fix**: no 503 happened this time |
| C3 | 5/5/5 | 5/5/5 | nothing |
| C4 | **3/3/3** | **5/5/5** | **the fix** |
| C5 | 10/10/9 | 10/**9**/**9** | slower API in two trials, not the fix |

*C4 after (trial 1)*, from `capstone_trials.py::c4`, and the log lines `serve.py::_write_log` wrote for the two inputs that used to crash:
```
- PASS · malformed · `no body` · HTTP 400 · curl 2 ms · id `4d52095d74b2` · HTTP 400
- PASS · malformed · `{}` · HTTP 400 · curl 2 ms · id `848aa9004d82` · HTTP 400
- PASS · malformed · `{"query": ""}` · HTTP 400 · curl 2 ms · id `6eb8a49929dd` · HTTP 400
- PASS · malformed · `{"query": 42}` · HTTP 400 · curl 2 ms · id `a338dc4959e9` · HTTP 400
- PASS · malformed · `["denim jacket"]` · HTTP 400 · curl 2 ms · id `6af1249990e4` · HTTP 400

{"ts": "2026-11-16T06:51:30.917+00:00", "request_id": "a338dc4959e9", "route": "/ask", "query": 42, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "'query' must be text, not int. Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", ..., "duration_ms": 0.1, "model_calls": 0, "tokens_total": 0}
{"ts": "2026-11-16T06:51:30.927+00:00", "request_id": "6af1249990e4", "route": "/ask", "query": null, "wardrobe": null, "status": 400, "outcome": "bad_request", "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", ..., "duration_ms": 0.1, "model_calls": 0, "tokens_total": 0}
```

*C5 after*, logged `duration_ms` of completed runs, sorted:
```
trial 1: 2003, 2149, 2302, 2727, 3151, 3938, 4474, 4633, 5198, 7067
trial 2: 2000, 2524, 2950, 3191, 3199, 3841, 4257, 5712, 8712, 11021
trial 3: 2052, 2957, 3175, 4684, 4881, 4953, 5646, 5834, 7856, 17769
```

**Did it help?** For C4, yes, completely: the two inputs that crashed every trial now get a 400 with a message saying what to send, and nothing that passed before broke. It did nothing for anything else, and I'm not claiming the C2 change. Under the same code, the 503 simply didn't happen in these 30 runs, so the C2 bug is still there (see below). C5 still met, but it got worse without any code change. The two slow runs were all model time: the `timings` show no `rate_limit_wait`, and `create_fit_card` alone took 16.5 s in the 17.8 s run. The tail I said in the verdicts was missing from the before trials turned up here. That also settles the "tighten C5 to 6 s" idea: 6 s would have missed in two of three after trials.

**What's Still Broken**

All five criteria are met after the change, so no target is still missed. One miss from the before trials was never fixed, though, and two targets were too loose.

**1. A temporary 503 from Gemini still kills the run (C2's before miss).** Unchanged: it passed after only because no 503 occurred. *What I'd do:* in `generate.py::generate`, treat `503`/`UNAVAILABLE` like a rate limit: retry with the existing backoff (`_retry_delay`, up to `MAX_RETRIES`) before raising `ModelUnavailable`. A bad key (`401`/"API key") should still fail at once, so C3 stays fast. To test it, I'd monkeypatch the Gemini client in a test so its first call raises a 503 on purpose, since waiting for Google to have a busy minute isn't a test. *Why I stopped:* the brief allows one improvement, and I chose the one I could prove. This is the first thing I'd do next (see below).

**2. The latency tail is real and I don't control it.** C5 passed, but two after trials only just made 9 of 10, and the latency stretch had 7 of 15 runs over 10 s. Every slow run is time spent inside one Gemini call, not my code. *What I'd do:* set a per-call timeout around 8 s and retry once, which is the same retry path as #1, so it should be built together with it. *Why I stopped:* it changes the meaning of "completed" (a retried card is a different card), and that deserves its own criterion.

**3. Targets I set too low.** C3 (bad key under 5 s): every one of 30 requests took 363 ms–1.2 s, so I'd tighten it to *under 2,000 ms*. C2's ±250 ms: every gap was 4–7 ms, so ±50 ms would still pass and would catch a timer that misses real work. C5 is *not* one I'd tighten after all; see The Improvement above.

**4. Out of scope, still true:** the no-item word list from unit 4, and ~1 s of every request spent starting `mcp_server.py` (latency stretch below).

**What I'd do next with another unit:** make `generate.py` retry `503 UNAVAILABLE` with backoff, tested by injecting a 503 on purpose. It's the only time in 60 matching-query runs that a valid request didn't get its fit card. The fix is ten lines in one function. And the same retry path is what a per-call timeout for the latency tail would need, so it unlocks the next fix too.





**How I Used AI**

I used Claude Code (Claude Opus 5.5) in VS Code for most of the capstone, so this section is about what it did and what I checked, not just two prompts.

*Moment 1: picking the stretch.* I pasted the capstone brief and asked it to "do a stretch feature that seems easiest". It picked the latency breakdown over the load test, a second improvement, or both run paths. Its reasons: the load test would hit the 15-requests-a-minute free-tier limit before it measured anything, and the other two each double a part of the unit. It added per-stage timers to `run_agent` and a separate rate-limit-wait counter in `generate.py`, so pacing time couldn't be mistaken for model time. Its first version printed every trace step during the timing runs, so it captured that output instead. The result I didn't expect was that 99.8% of the search stage is starting the MCP process.

*Moment 2: building and testing the extension.* I asked it to do as much of the required capstone as it could while I was busy. It built the structured log in `serve.py`, wrote RUNNING.md and tested it from a fresh clone, measured cost from the log, and wrote and ran the trial harness. Two things it found that I wouldn't have predicted. First, the documented `python serve.py` command can't work on a Mac, because AirPlay owns port 5000 and answers with a 403. It only showed up when the cost runs used the real default port; the clean-clone test had used a spare one. Second, `{"query": 42}` crashes the starter's validation with a 500. It also caught three wrong numbers in the reasons of its own criteria draft. It added a correction note underneath instead of editing the committed text, and didn't change any target.

Claude drafted the five capstone criteria from my system's known weak points; I reviewed them before any trial ran.

**Stretch: Latency Breakdown**

I'm adding the latency-breakdown stretch, which measures where the time goes across the stages of one run. `run_agent()` in [agent.py](agent.py) now records wall-clock milliseconds for each stage in `session["timings"]`: `parse_query`, `search_listings_mcp`, `suggest_outfit`, `create_fit_card` and `total`. Model stages also record how much of their time was spent asleep on the rate limiter (`<stage>.rate_limit_wait`, counted in [generate.py](generate.py)), so a slow model and a run that was just waiting its turn can be told apart. A failed stage still gets its time recorded. `python latency_breakdown.py` runs the five matching queries three times each with the cache off. It also times the same search in-process to show how much of the search stage is the MCP process start rather than the search itself. It writes the table to `results/latency_<timestamp>.md`.

I ran `python latency_breakdown.py` on 2026-11-15: 15 runs (3 rounds × the 5 matching queries), cache off, an 8-second gap between runs, model `gemini-3.5-flash-lite`. All 15 runs completed all three tools. Full per-run table: [results/latency_2026-11-15_2231.md](results/latency_2026-11-15_2231.md).

| Stage | Mean (ms) | Median | Min | Max | Share of mean total |
|---|---|---|---|---|---|
| parse_query | 0 | 0 | 0 | 2 | 0.0% |
| search_listings_mcp | 962 | 554 | 335 | 3,086 | 10.4% |
| suggest_outfit | 4,457 | 2,726 | 769 | 12,223 | 48.0% |
| create_fit_card | 3,870 | 1,022 | 587 | 14,737 | 41.7% |
| total | 9,290 | 8,668 | 1,820 | 26,038 | 100.0% |
| *of which: rate_limit_wait* | 0 | 0 | 0 | 0 | — |
| *search, in-process (no MCP)* | 2 | 2 | 1 | 3 | — |
| *MCP overhead (mcp − in-process)* | 960 | 552 | 333 | 3,085 | — |

What it shows:

- **The two model calls are ~90% of the time** (48.0% + 41.7% of the mean total). Parsing is effectively free, and the loop code between stages added no measurable time (0 ms unaccounted).
- **None of it was our rate limiter.** `rate_limit_wait` was 0 in all 15 runs, so the 8-second gap kept `generate.py` from ever pausing and no 429 backoff happened. The model time is time spent waiting on the API call itself. This measures it from the client side, so I can't split network time from the model's generation time.
- **The model time varies a lot, and it doesn't depend on the query.** Round 1 was fast for every query (1.8–2.8 s total). Rounds 2 and 3 were much slower for the same five queries. `platform sneakers size 8` took 2.0 s in round 1, then 22.9 s and 26.0 s. Since identical inputs ranged over 13×, the spread comes from the service's response time, not prompt size or which item was found. That's why the mean (9.3 s) is above the median (8.7 s), and why the worst run was 14× the best.
- **The search stage is almost all MCP overhead.** The search itself takes 2 ms in-process. Over MCP it averaged 962 ms, so 99.8% of that stage is starting `mcp_server.py` as a fresh Python process and connecting to it on every call. That overhead also wandered (335 ms to 3.1 s), slowest in round 2. Model calls never overlap with the search, so that variation is my laptop's process-startup time, not the network.

If I had to make a run faster, the model calls are where the time is, but I can't control their spread. The one cost fully under my control is the ~1 s MCP startup, which a long-lived MCP connection would remove. It's 10% of the mean run and up to 3 s on a slow one.
