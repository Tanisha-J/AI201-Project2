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

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
