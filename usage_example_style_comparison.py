"""Aggregation of already-existing per-sentence-style outputs into comparison
tables for two findings that need no new computation, only summarization:

- Pronoun-elaboration effect (1.5): sentence_style 1 (no pronoun) vs. 2 (with
  an explicit anaphoric pronoun clause).
- Trans-identity effect (1.3): sentence_style 1 vs. 3 (trans-marked, no
  pronoun) and 2 vs. 4 (trans-marked, with pronoun).

Reads outputs/<model>/<model>_error_analysis_sentence_style_{1,2,3,4}.csv
(already produced by usage_example_process_data.py) and writes two summary
CSVs to outputs/summary/. No new translations, no new pipeline runs.
"""

import os
import pandas as pd

OUTPUTS_ROOT = "./outputs"
SUMMARY_DIR = os.path.join(OUTPUTS_ROOT, "summary")
MODELS = ["google", "google_llm", "deepl", "microsoft", "systran", "gpt-4o"]


def load_style_accuracy(model: str, style: int) -> dict[str, float] | None:
    path = os.path.join(OUTPUTS_ROOT, model, f"{model}_error_analysis_sentence_style_{style}.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, index_col=0)
    languages = df.loc["language"].tolist()
    accuracy = df.loc["accuracy"].astype(float).tolist()
    return dict(zip(languages, accuracy))


def build_comparison(style_a: int, style_b: int, label_a: str, label_b: str) -> pd.DataFrame:
    rows = []
    for model in MODELS:
        acc_a = load_style_accuracy(model, style_a)
        acc_b = load_style_accuracy(model, style_b)
        if acc_a is None or acc_b is None:
            continue
        for lang in acc_a:
            if lang not in acc_b:
                continue
            rows.append(
                {
                    "model": model,
                    "language": lang,
                    f"accuracy_{label_a}": acc_a[lang],
                    f"accuracy_{label_b}": acc_b[lang],
                    "diff_pp": (acc_b[lang] - acc_a[lang]) * 100,
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(SUMMARY_DIR, exist_ok=True)

    pronoun_df = build_comparison(1, 2, "baseline", "pronoun")
    pronoun_df.to_csv(os.path.join(SUMMARY_DIR, "pronoun_effect_comparison.csv"), index=False)
    print("Saved pronoun_effect_comparison.csv")
    print(pronoun_df.sort_values("diff_pp", ascending=False).to_string(index=False))

    trans_df = build_comparison(1, 3, "baseline", "trans")
    trans_pron_df = build_comparison(2, 4, "baseline_pronoun", "trans_pronoun")
    trans_df.to_csv(os.path.join(SUMMARY_DIR, "trans_effect_comparison.csv"), index=False)
    trans_pron_df.to_csv(os.path.join(SUMMARY_DIR, "trans_effect_pronoun_comparison.csv"), index=False)
    print("\nSaved trans_effect_comparison.csv + trans_effect_pronoun_comparison.csv")
    print(trans_df.sort_values("diff_pp", ascending=False).to_string(index=False))
