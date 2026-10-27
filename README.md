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
| `assertion_reaction` | 140 | 70% |
| `inquiry` | 37 | 18.5% |
| `evidenced_claim` | 23 | 11.5% |
| **Total** | 200 | 100% |

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

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42

**Device:** cpu

**Anything I changed from the defaults, and why:** Nothing. I ran the defaults.

**Split sizes:** train 139 · val 31 · test 30

| Label | Train | Val | Test |
|---|---|---|---|
| `assertion_reaction` | 97 | 22 | 21 |
| `evidenced_claim` | 17 | 3 | 3 |
| `inquiry` | 25 | 6 | 6 |

`evidenced_claim` has only 3 test examples and `inquiry` only 6, both below the roughly 8 needed for stable metrics. Their scores will move a lot between seeds, and a single prediction changes `evidenced_claim`'s recall by about 33 points.



---

## How I Used AI

- *What I asked for:* I gave Claude my label definitions and asked for eight posts that sit on my label boundaries, then classified them myself using only my written rules.
- *What came back:* Eight borderline posts. Classifying them showed two contradictions in my rules: one rule said a question with a rhetorical angle was still `inquiry` and another said rhetorical questions were not, and a post whose only number was a player's age didn't fit my evidence rule cleanly.
- *What I changed:* I made intent win over form for questions (the intent-wins rule) and added the exception that a background figure like an age doesn't count as evidence (the direct-anchor rule). None of the eight generated posts are in my dataset.

**Moment 2**

- *What I asked for:* I pasted my five acceptance criteria and asked whether each could be checked by someone who couldn't ask me what I meant, plus one reason each target might be too easy and one it might be too hard, without suggesting new numbers.
- *What came back:* It flagged wording that made some criteria uncheckable, such as "macro recall" for a single label, two different conditions in one criterion, and a self-agreement criterion with no cool-off period stated.
- *What I changed:* [Describe the wording fixes you made in criteria.md. The numbers are my own.]

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

Both models scored on the same 30 held-out posts in `test_split.csv` (21 `assertion_reaction`, 6 `inquiry`, 3 `evidenced_claim`). The baseline is `facebook/bart-large-mnli` zero-shot, run locally on CPU, prompted with the three definitions in `label_definitions.txt`. The trained column is `results.json` (seed 42, the unit 5 run). Output of `python baseline.py --trained results.json`:

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.200 | 0.700 | +0.500 |
| Macro F1 | 0.247 | 0.275 | +0.027 |
| F1 — `assertion_reaction` | 0.091 | 0.824 | +0.733 |
| F1 — `evidenced_claim` | 0.207 | 0.000 | -0.207 |
| F1 — `inquiry` | 0.444 | 0.000 | -0.444 |

**What my definitions were worth, measured.** I ran the baseline twice on the same 30 posts, once with my definitions and once with bare label names:

| Baseline prompt | Accuracy | Macro F1 | F1 `assertion_reaction` | F1 `evidenced_claim` | F1 `inquiry` |
|---|---|---|---|---|---|
| Bare label names | 0.300 | 0.377 | 0.174 | 0.231 | 0.727 |
| My definitions (reported above) | 0.200 | 0.247 | 0.091 | 0.207 | 0.444 |

My definitions made the zero-shot model **worse by 10 points of accuracy**. Both runs put almost everything into `evidenced_claim`: 26 of 30 posts with definitions and 23 of 30 with bare names. The NLI model reads "This post is a claim backed by at least one explicit figure…" as entailed by nearly any confident sentence. It also handles the negation in my `assertion_reaction` definition ("…that offers **no** checkable support") badly, so that label almost never wins (1 of 21 caught). The table above uses the definitions run, because that is the fair opponent the brief asks for.

**What I predicted before I looked:**
<!-- TODO(Viraj): write your one-sentence prediction here, in your own words. -->

**What the gap actually means:** The +0.50 accuracy gap is not fine-tuning learning my labels. The trained model predicts `assertion_reaction` for all 30 posts, so its 0.700 is exactly the share of the majority class (21/30). On the two labels that need the model to read anything, the zero-shot baseline beats it: `inquiry` F1 0.444 vs 0.000, and `evidenced_claim` F1 0.207 vs 0.000. Macro F1 is close to a tie (0.247 vs 0.275). As trained in unit 5, my fine-tuning bought a majority-class prior and nothing else. The baseline's advantage costs time, though: about 1–2 s per post on CPU, plus a 1.6 GB model, against milliseconds for the fine-tuned one.

---

## Run Log — Before

Notebook section 6, defaults (3 epochs, lr 2e-5, batch 16, max length 128), seeds 42 / 7 / 2024. **Device: `cpu` (torch 2.14.1+cpu).** Seed 42 reproduces `results.json` exactly.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.700 | 0.700 | 0.700 | MET (hollow — see verdicts) |
| 2. Recall on `inquiry` | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |
| 3. Recall on `evidenced_claim` | ≥ 0.70 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Precision on `assertion_reaction` | ≥ 0.68 | 0.700 | 0.700 | 0.700 | MET (hollow — see verdicts) |
| 5. Self-agreement, 20 cold posts re-labelled | ≥ 0.85 | n/a (not seed-dependent) | | | PENDING |

The notebook's spread table:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.700 | 0.700 | 0.700 | 0.000 |
| Macro F1 | 0.275 | 0.275 | 0.275 | 0.000 |
| F1 — `assertion_reaction` | 0.824 | 0.824 | 0.824 | 0.000 |
| F1 — `evidenced_claim` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `inquiry` | 0.000 | 0.000 | 0.000 | 0.000 |

The notebook says "Accuracy moved 0.000 across seeds. Stable enough to trust." That is misleading here. The three numbers are identical because all three models make the same constant prediction, and every stratified split has the same 21/3/6 test mix. A zero spread here is a symptom, not reassurance. Validation accuracy was 0.710 (22/31, the majority rate) on every epoch of every seed. Final training loss was 0.88 / 0.92 / 0.89, roughly the entropy of my label prior (≈0.81). The model learned the class frequencies and stopped.

### Confusion matrix

Section 7 output, seed 42:

| true \ predicted | assertion_reaction | evidenced_claim | inquiry |
|---|---|---|---|
| **assertion_reaction** | 21 | 0 | 0 |
| **evidenced_claim** | 3 | 0 | 0 |
| **inquiry** | 6 | 0 | 0 |

Summed over all three seeds (90 test predictions):

| true \ predicted | assertion_reaction | evidenced_claim | inquiry |
|---|---|---|---|
| **assertion_reaction** | 63 | 0 | 0 |
| **evidenced_claim** | 9 | 0 | 0 |
| **inquiry** | 18 | 0 | 0 |

**My biggest off-diagonal number, and what it means:** 6 real `inquiry` posts were called `assertion_reaction`, and 0 went the other way. It is the same on every seed (18 of 18 across all three). The model never learned the inquiry/assertion boundary in either direction; it learned to say `assertion_reaction` every time. This is not one confused pair: the whole first column is full, and the other two columns are empty.

---

## Verdicts and Diagnoses

A target has to hold on all three seeds.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 | MET (hollow) | 0.700 on all three seeds clears 0.65. But a model that outputs `assertion_reaction` for everything scores exactly 0.700 on these splits, so the criterion passed without the model learning anything. My unit 5 reason assumed a majority-class guesser would score about 0.40 (from my reading log). In my real 200 rows the majority class is 70%, so 0.65 sits **below** the trivial baseline. I am leaving the number as written and reporting the problem rather than quietly raising the bar after the fact. |
| 2 | Recall on `inquiry` (revised wording, same 0.60) | ≥ 0.60 | MISSED | 0.000 / 0.000 / 0.000. Not one of 18 test inquiries across three seeds was caught. Wording revised in `criteria.md`, because "macro recall for a single label" can't be computed. The target number is unchanged. |
| 3 | Recall on `evidenced_claim` | ≥ 0.70 | MISSED | 0.000 / 0.000 / 0.000, 0 of 9. |
| 4 | Precision on `assertion_reaction` | ≥ 0.68 | MET (hollow) | 0.700 on all three. When a model predicts one label for everything, that label's precision equals its base rate (21/30), so this also passes for a model that learned nothing. |
| 5 | Self-agreement on the 20 cold posts | ≥ 0.85 | PENDING | Needs me to re-label the 20 cold posts blind. They are in `self_agreement_relabel.csv` (shuffled, no labels); `python score_self_agreement.py` scores it. <!-- TODO(Viraj): fill in after relabelling. --> |

**Diagnoses**

**Criteria 2 and 3 (minority recall = 0): a training problem (too few optimizer steps on lopsided data), not a labelling problem.**

- *What the numbers show:* both minority labels score 0 on all three seeds, with no variation at all. The confusion matrix has no off-diagonal structure that points at a boundary; every row goes to `assertion_reaction`. Validation accuracy was flat at the majority rate across all 3 epochs, and training loss ended near the entropy of the label prior. With 139 training rows and batch size 16, three epochs are only 27 optimizer steps at lr 2e-5. On 70/18/12 data the cheapest way to lower the loss in 27 steps is to learn the prior.
- *Why I don't think it's labelling:* if I had applied a boundary two different ways, the matrix would show one specific pair leaking, in one direction, with the rest learned. Here even `inquiry` fails, and it is my most surface-marked label (almost every one ends in "?"). The baseline gets 4/6 of those with bare label names. A model that had actually trained on that signal would not miss all 18. The agreement report points the same way: applied to someone else's written rules, the load-bearing-fact rule (staff rule 1, the direct counterpart of my own direct-anchor rule) was applied the same way as staff on all 30 posts, with no pile (a) cases.
- *Caveat on that evidence:* the staff-set labels were produced with Claude's help (see How I Used AI), so the 100% is evidence that the rule is applicable, not proof that **my** 200 labels were consistent. The only direct evidence on my own consistency is hard case 1 in The Dataset: I flipped "He clears Bellingham statistically…" from `evidenced_claim` to `assertion_reaction` on review. That means my evidence boundary is not perfectly stable. It cannot explain a collapse that also hits `inquiry`, though. Criterion 5's relabel is the test that would settle it.
- *Contributing cause: too few examples.* Even once the model learns, `evidenced_claim` has only 3 test posts per seed (one post = 33 points of recall) and only 17 training examples. Its score will be noisy whatever the fix.

**Criteria 1 and 4: met, but on a broken measure.** Both pass for a constant predictor. That is a finding about my criteria rather than the model. My unit 5 targets were calibrated on a 35-post reading log with a much flatter label mix than the 200 I actually collected.

---

## Agreement Report

I labelled the 30 staff posts under `data/staff_taxonomy.md` and saved them to `my_staff_labels.csv` before opening the answer key. Then I ran `python agreement.py --staff-labels data/data_staff_labels.csv` (the TF's file arrived under that name).

**Agreement rate:** 30 / 30 = 100%

**Disagreements**

None. All 30 posts matched staff, and `agreement_results.json` records 0 disagreements and 0 unmatched posts.

**Was the set easy, or is the rule tight?** Mostly the rules are tight, and a few posts tested them. Each label has a clear core: ten posts that argue from data the writer gathered, ten bare general claims, and ten first-person moments. The posts that could have gone either way were the ones the decision rules were written for, and each rule decided its case:

- **sp_014**, *"Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story…"*: it has a figure but is `hot_take`. This is the staff's own rule 1 example almost word for word. The 3% decorates a conclusion the writer has already reached ("obviously… the whole story").
- **sp_018**, *"Track sessions are wasted on anyone running slower than 8 minute miles."*: `hot_take`. "8 minute miles" is a threshold inside the claim, not evidence for it. Under rule 1 it carries no argument.
- **sp_021**, *"Four minutes off. FOUR…"* and **sp_027**, *"…leaning at about 20 degrees"*: both `reaction`. The numbers describe what just happened to the writer; nothing general is argued from them (rules 2 and 3).
- **sp_005** and **sp_010**: one-runner or three-runner anecdotes with figures. Both `analysis`, because the figure is the reason given against the general claim ("carbon plates aren't the whole story", "shoes do less than the noise"). The definition asks for a load-bearing checkable fact, not a large sample.
- **sp_029**, *"Just realised the shoes I set every PB in… are the wrong size"*: `reaction`, not an implied `hot_take` about shoes. It reports something about the writer and makes no general claim (rule 2).

**What the pattern in my disagreements tells me:** There is no pile (a), (b) or (c) to sort. The useful finding is which rule did the work. Staff rule 1 ("does the fact carry the argument?") decided both of the trickiest posts, and it is the same question as my own direct-anchor rule. So the evidence/assertion boundary in my taxonomy is checkable when it is written down this sharply. That supports the diagnosis above: the model's failure is not a symptom of an unappliable boundary.


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
