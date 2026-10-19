# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments and posts from r/LaLiga, the Reddit community for Spain's top football league, by what each post is doing. A post is an inquiry if it genuinely asks the community something, an evidenced_claim if it backs its claim with an explicit, checkable figure, and an assertion_reaction otherwise: opinions, hot takes, banter and reactions. The aim is to separate posts that argue from evidence from posts that just assert, without losing the questions people ask along the way.



---

## Label Taxonomy

Posts are labelled by checking these in order and stopping at the first match:

1. Does the post genuinely ask the community for information, advice, or open opinions, rather than asserting the author's own conclusion? → `inquiry`
2. Does the post back its claim with an explicit, checkable figure that directly supports it? → `evidenced_claim`
3. Everything else → `assertion_reaction`

Excluded from the dataset: bot posts, news-link titles with no user commentary, and bare score posts. If a user adds their own commentary to a link, only their text is labelled.

### `inquiry`

**Definition:** An open question seeking information, advice, or the community's opinions, without asserting the author's own answer. Rhetorical questions where the author expresses a pre-baked conclusion (e.g., *"Isn't it obvious...?"*, *"How is nobody talking about him??"*) fail Step 1 and skip to Step 2 or Step 3 based on whether they contain explicit supporting stats or unbacked assertions.

**Example 1:**
Can someone bring me up to date on Rayo Vallecano?

**Example 2:**
Who's been the best keeper in La Liga this season outside Courtois? Genuinely curious.

### `evidenced_claim`

**Definition:** A claim backed by at least one explicit figure (a stat value, fee, age, league position, or contract term) that directly supports it; naming a match, team, or stat category without a value is context, not evidence.

**Example 1:**
Villarreal sold 3 starters this summer for over €40m total and they are still 5th in the table.

**Example 2:**
Girona scored 85 goals last season in La Liga, which was second only to Real Madrid.

### `assertion_reaction`

**Definition:** An opinion, judgment, hot take, or reaction that offers no checkable support.

**Example 1:**
Most underrated player in the world right now, period.

**Example 2:**
Watched the Getafe game on Sunday. Their midfield is the worst in the league, not even close.

### The hardest boundary

**Which two labels:** `evidenced_claim` and `assertion_reaction`

**Borderline post:**
He clears Bellingham statistically but no one talks about him and people won't shut up about Bellingham.

**The decision rule I used every time:** A post is `evidenced_claim` only if it states the figure itself. Saying the stats are good ("clears him statistically", "xG through the roof") without giving a value is `assertion_reaction`. Additionally, an explicit number that serves merely as background metadata (such as a player's age in *"Lamine is 17 and already has more assists than half the wingers"*) does not count as evidence unless the figure directly quantifies the primary statistical claim.



---

## The Dataset

**Where the posts came from:** Public threads on r/LaLiga, read on old.reddit.com. The posts come from a match preview thread, discussion of the Negreira case, the Arda Güler red-card debate, a thread on Barcelona's start to the season, the Babylon Park and Camp Nou sponsorship story, Real Madrid's summer rebuild and Mourinho's return, a question about watching La Liga in Canada, a post-international-break "which match are you looking forward to" thread, an all-time La Liga XI thread, and a thread about Dani Olmo's future.

[How you collected them: copied by hand, or saved thread pages and parsed them with a script. Mention that scripted collection from Reddit's JSON endpoints was blocked (HTTP 403), if you want to include that.]

**How I labelled them:** The first 20 rows were labelled cold, by me alone with only my written definitions, and are marked `cold` in the note column. [Say how you labelled the rest: by hand, or pre-labelled with an AI tool and then read and corrected one by one. Mark any pre-labelled rows in the note column.] Where my label conflicted with my own written rules, I corrected it to follow the rule and recorded the original label in the note.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
|`assertion_reaction`  | 153 | 76 |
| `evidenced_claim` | 24 | 14 |
| `inquiry` | 23 | 12 |
| **Total** |  | 100% |

**Three hard cases**

**1.**
> *The post:* "He clears Bellingham statistically but no one talks about him and people won't shut up about Bellingham."
>
> *Could have been:* `evidenced_claim` or `assertion_reaction`
>
> *I chose, because:* `assertion_reaction`. It appeals to statistics but never states one, so it fails the direct-anchor rule. I labelled it `evidenced_claim` when labelling cold and corrected it against my own rule, which tells me this is the boundary I am most likely to apply inconsistently.

**2.**
> *The post:* "Do people forget how extremely poor and embarrassing Mourinhos first stint at Real Madrid was?"
>
> *Could have been:* `inquiry` or `assertion_reaction`
>
> *I chose, because:* `assertion_reaction`. It is phrased as a question, but the author has already given the answer ("extremely poor and embarrassing"). Under the intent-wins rule a rhetorical question skips step 1, and it contains no figure, so it falls to step 3.

**3.**
> *The post:* "They didn't reinforce that much quality wise. They didn't go all in for rodri. Broke the bank on a 19y old that still has to prove himself and the rest is hardly worth mentioning."
>
> *Could have been:* `evidenced_claim` or `assertion_reaction`
>
> *I chose, because:* `assertion_reaction`. The only figure is the player's age, which is background rather than support for the claim that Madrid didn't add quality. The direct-anchor rule says that doesn't count as evidence.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
