"""End-to-end usage example for the deval_mt package, on a small toy dataset
(not tied to any study's data -- copy this and swap in your own sentences).

Install the package first: `pip install -e .` from the repo root (see
README.md's "Installation" section), plus the Spanish spaCy model used here:
`python -m spacy download es_dep_news_trf`.

Run from the repository root: `python deval_mt/usage_example.py`.
"""

import pandas as pd

from deval_mt import (
    DEvalDataset,
    SpaCyMorphAnalyzer,
    run_subject_pipeline,
    evaluate_processed_dataset,
    ErrorAnalysis,
)

OUTPUT_DIR = "deval_mt_usage_example_output"

# ---------------------------------------------------------------------------
# 1. Build a dataset. Required columns: your source text, a `<subject>_idx`
# column (integer position of the subject noun in `text.split()`), an
# `adjective` column ("none", or anything else if an adjective precedes the
# noun -- see README.md's "Using a different source language" section), and
# a gold gender column. `x_stereotypical` is optional (0-1, how stereotype-
# congruent the occupation is) -- only needed if you want the logistic
# regression / stereotypicality plot.
# ---------------------------------------------------------------------------
df = pd.DataFrame(
    {
        "text": [
            "Der Bauer geht gerne zur Arbeit.",
            "Die Bäuerin geht gerne zur Arbeit.",
            "Der Arzt untersucht den Patienten.",
            "Die Ärztin untersucht den Patienten.",
            "Der Erzieher betreut die Kinder.",
            "Die Erzieherin betreut die Kinder.",
        ],
        "x_idx": [1, 1, 1, 1, 1, 1],
        "adjective": ["none"] * 6,
        "x_gender": ["MASCULINE", "FEMININE"] * 3,
        # real-world stereotypicality: how male- or female-coded the
        # occupation is, matching the gold gender each row already carries
        # (a farmer/doctor skewing male, a childcare worker skewing female).
        "x_stereotypical": [0.79, 0.21, 0.68, 0.32, 0.25, 0.75],
    }
)

dataset = DEvalDataset(df, text_column="text")

# Translations: supply your own MT output. tools/automized_translations/ has
# ready-made fetchers (DeepL, GPT, SYSTRAN, Google, Microsoft) if you'd
# rather generate these than hand-write them -- see README.md.
dataset.add_translations(
    "es",
    [
        "Al campesino le gusta ir a trabajar.",
        "A la campesina le gusta ir al trabajo.",
        "El médico examina al paciente.",
        "La médica examina al paciente.",
        "El educador cuida a los niños.",
        # Deliberately mistranslated (masculine default, ignoring the
        # feminine gold "Erzieherin") -- gives the toy dataset one real
        # error, so the plots below aren't all-100%-correct and the
        # logistic regression has something to fit.
        "El educador cuida a los niños.",
    ],
)

# ---------------------------------------------------------------------------
# 2. Run the pipeline: aligns source/target, extracts the translated
# subject phrase, predicts its grammatical gender. One analyzer per
# language you're evaluating.
# ---------------------------------------------------------------------------
analyzer = SpaCyMorphAnalyzer("es_dep_news_trf")
analyzer.load()

dataset = run_subject_pipeline(
    dataset,
    analyzers={"es": analyzer},
    source_column="text",
    subject_index_column="x_idx",
)

print(dataset.df[["text", "x_phrase_es", "x_gender_es"]].to_string(index=False))

# ---------------------------------------------------------------------------
# 3. Evaluate: scores predictions against gold, and (with plot_dir/
# output_dir set) writes the full report -- error-analysis table, gold-
# >predicted Sankey diagram, and the stereotypicality curve -- to disk.
# ---------------------------------------------------------------------------
results = evaluate_processed_dataset(
    dataset,
    gold_col="x_gender",
    predictor_col="x_stereotypical",
    plot_dir=OUTPUT_DIR,
    output_dir=OUTPUT_DIR,
)

print("\nAccuracy per language:")
print(results["error_analysis"][["language", "total", "correct", "accuracy"]])

print("\nStereotype-congruence odds ratio (es):")
print(results["logistic_regression"][["language", "odds_ratio", "p_value", "significance"]])

# ---------------------------------------------------------------------------
# 4. Optional: compare accuracy between two groups instead of one pooled
# number. First, label each row "stereotype_congruent" or
# "counter_stereotype" based on x_stereotypical. Then ErrorAnalysis.grouped
# computes accuracy separately for each label -- so you get two accuracy
# numbers (one per group) instead of one number averaged over everything.
# Swap "congruent" for any other column to compare different groups (e.g.
# sentence style, a demographic axis).
# ---------------------------------------------------------------------------
dataset.df["congruent"] = dataset.df["x_stereotypical"].apply(
    lambda p: "stereotype_congruent" if p > 0.5 else "counter_stereotype"
)
grouped_results = ErrorAnalysis.grouped(
    dataset,
    "x_gender",
    scope="congruence_check",
    group_col="congruent",
    group_labels={"stereotype_congruent": "congruent", "counter_stereotype": "counter"},
)
print("\nAccuracy split by stereotype-congruence (toy example, 3 rows/group):")
print(pd.concat(grouped_results)[["language", "pairing", "total", "accuracy"]])
