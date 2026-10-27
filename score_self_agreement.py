#!/usr/bin/env python3
"""
Criterion 5: self-agreement on the 20 cold posts.

Fill the `label` column of self_agreement_relabel.csv blind (don't look at
labels.csv), then run:

    python score_self_agreement.py
"""
import json
import sys

import pandas as pd

original = pd.read_csv("labels.csv")
original = original[original["note"] == "cold"].set_index("text")["label"]
relabel = pd.read_csv("self_agreement_relabel.csv").set_index("text")["label"]

if relabel.isna().any() or (relabel.astype(str).str.strip() == "").any():
    sys.exit("Some rows in self_agreement_relabel.csv have no label yet.")

joined = pd.DataFrame({"original": original, "relabel": relabel.astype(str).str.strip()}).dropna()
agreed = (joined["original"] == joined["relabel"]).sum()
rate = agreed / len(joined)

print(f"{agreed} / {len(joined)} = {rate:.0%}   (target >= 85%: {'MET' if rate >= 0.85 else 'MISSED'})")
for text, row in joined[joined["original"] != joined["relabel"]].iterrows():
    print(f"\n- {text[:90]}\n  then: {row['original']}   now: {row['relabel']}")

with open("self_agreement_results.json", "w", encoding="utf-8") as f:
    json.dump({"compared": int(len(joined)), "agreed": int(agreed), "rate": float(rate),
               "disagreements": [{"text": t, "original": r["original"], "relabel": r["relabel"]}
                                 for t, r in joined[joined["original"] != joined["relabel"]].iterrows()]},
              f, indent=2)
print("\nWrote self_agreement_results.json.")
