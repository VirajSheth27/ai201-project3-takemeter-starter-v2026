# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall Accuracy Baseline Standard

Overall accuracy must reach at least 0.65 on the held-out test set across all three seeds.

**Why this target:** A majority-class baseline that always predicts `assertion_reaction` yields an accuracy of roughly 0.40 (14/35 posts in our reading log). Setting the target at 0.65 requires the classifier to meaningfully learn distinct lexical and structural features across classes rather than defaulting to the majority class.

---

## 2. Inquiry Per-Label Recall

The macro recall for the `inquiry` label must be at least 0.60 on the held-out test set across all three seeds.

**Why this target:** In our reading log, `inquiry` represents only ~23% of posts (8 out of 35). Because `inquiry` is a smaller minority class compared to `assertion_reaction` and `evidenced_claim`, a lower recall threshold accounts for fewer test examples while ensuring the model still reliably captures true questions and help requests without collapsing them into discussion hot takes.

> **Revised in unit 6:** The recall for the `inquiry` label must be at least
> 0.60 on the held-out test set across all three seeds.
>
> **Why revised:** "Macro recall" is an average over several labels, so "the
> macro recall for the `inquiry` label" names no number I can compute — macro
> recall over all three labels and `inquiry`'s own recall are different
> figures, and the original could be read as either. The intent was always
> `inquiry`'s own recall, which is what the per-label block in
> `results_three_seeds_*.json` reports. The target (0.60) is unchanged.


---

## 3. Hardest Boundary Recall (Evidenced Claim)

The recall for `evidenced_claim` must reach at least 0.70 on the held-out test set across all three seeds, tolerating no more than 30% of true evidenced posts being misclassified as `assertion_reaction`.

**Why this target:** The hardest boundary in our taxonomy is distinguishing `evidenced_claim` from `assertion_reaction` when posts contain subtle numerical figures or metrics. A 0.70 recall ensures the model successfully detects explicit supporting data (e.g., pass stats, transfer fees, clean sheets) without excessively defaulting to unbacked hot takes.


---

## 4. Precision Balance on Assertion Reaction

The precision for `assertion_reaction` must be at least 0.68 on the held-out test set across all three seeds.

**Why this target:** Because `assertion_reaction` serves as our default fallback category (Priority 3 in the decision tree), an over-eager model might dump ambiguous queries or stat posts into this bucket. Setting a minimum precision of 0.68 ensures that posts labeled as unbacked hot takes or reactions are genuinely unevidenced and non-query statements.


---

## 5. Intra-Annotator Labeling Consistency (Self-Agreement)

The intra-annotator agreement rate (percentage of matching labels) must be at least 0.85 when re-labeling 20 cold posts after a cool-off period.

**Why this target:** Because judgment calls around rhetorical queries and unanchored metrics (e.g., player age vs. stat direct anchors) can introduce human drift, achieving an 85% self-agreement rate proves that our strict priority rules (*Intent Wins* and *Direct Anchor*) produce repeatable and reliable annotations.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->