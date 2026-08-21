"""Analysis for processed_data/<model>_processed.csv.

Run from the repository root: `python study/usage_example_process_data.py`.

Two stages -- each just wires SDK functions together, no analysis logic
lives in this file:

1. `evaluate_model`, once per model: `ErrorAnalysis.grouped` writes one
   consolidated <model>_error_analysis.csv (see scope_specs below), plus one
   call each for the confusion matrix, logistic regression, stereotypicality
   plot, names composition plot, and the two significance tests. Written to
   study/outputs/<model>/.
2. `build_summary`, once all models are done: pure aggregation of the CSVs
   stage 1 already wrote -- no new computation. Written to
   study/outputs/summary/.
"""

import os

import pandas as pd

from deval_mt import (
    DEvalDataset,
    ErrorAnalysis,
    ConfusionMatrix,
    LogisticRegressionAnalysis,
    test_direction_skew,
    test_paired_gap,
    plot_gender_composition,
    plot_stereotypicality,
    plot_accuracy_heatmap,
    format_significance_table,
    compare_accuracy_by_language,
    save_dataframes,
)

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
PROCESSED_DIR = "./study/processed_data"
OUTPUTS_ROOT = "./study/outputs"
SUMMARY_DIR = os.path.join(OUTPUTS_ROOT, "summary")


def load_processed_dataset(model_name: str, languages: list[str]):
    processed_file = os.path.join(PROCESSED_DIR, f"{model_name}_processed.csv")
    if not os.path.exists(processed_file):
        raise FileNotFoundError(
            f"Processed dataset '{processed_file}' not found. This script does not rebuild datasets."
        )

    print(f"[{model_name}] Loading processed dataset from {processed_file}")
    df = pd.read_csv(processed_file, sep=";")

    available_translation_columns = [lang for lang in languages if lang in df.columns]
    available_prediction_columns = [lang for lang in languages if f"x_gender_{lang}" in df.columns]

    if not available_prediction_columns:
        raise RuntimeError(f"No x_gender columns found in '{processed_file}'.")

    return df, available_translation_columns, available_prediction_columns


def make_dataset(df_subset: pd.DataFrame, translation_cols: list[str], prediction_cols: list[str]) -> DEvalDataset:
    ds = DEvalDataset(df_subset, text_column="text")
    ds.translation_columns = {lang: lang for lang in translation_cols}
    ds.prediction_columns = {lang: f"x_gender_{lang}" for lang in prediction_cols}
    return ds


def significance_neutral_names(df_subset: pd.DataFrame, languages: list[str], model_name: str) -> pd.DataFrame:
    """For neutral-name sentences (style 6, name_gender == 'n'), the gold
    gender is genuinely ambiguous -- the name gives no cue either way.
    Binomial test per language, over just the WRONG predictions: when the
    pipeline does get it wrong, is the direction it defaults to (->
    MASCULINE vs. -> FEMININE) skewed away from a random 50/50 split? Tests
    error direction, not accuracy -- says nothing about how often errors
    happen, only which way they lean when they do."""
    rows = []
    for lang in languages:
        pred_col = f"x_gender_{lang}"
        if pred_col not in df_subset.columns:
            continue
        errors = [
            (gold, pred)
            for gold, pred in zip(df_subset["x_gender"], df_subset[pred_col])
            if pd.notna(pred) and gold != pred and pred in ("MASCULINE", "FEMININE")
        ]
        result = test_direction_skew(errors)
        result["language"] = lang
        result["model"] = model_name
        rows.append(result)
    return pd.DataFrame(rows)


def significance_heteronormativity(df_subset: pd.DataFrame, languages: list[str], model_name: str) -> pd.DataFrame:
    """For romantic sentences (style 5), the subject's own gold gender is
    grammatically unambiguous (e.g. "the farmer" is definitely masculine or
    feminine on its own) -- only the romantic partner's gender varies.
    McNemar's test per language: is the subject's gender translated LESS
    ACCURATELY when the partner is same-gender-coded vs. different-gender-
    coded? Tests whether an unrelated cue (implied sexual orientation) leaks
    into a translation that shouldn't depend on it at all -- accuracy, not
    error direction (contrast with significance_neutral_names above). Paired
    design: every subject sentence (sentence_id, x_nom_sg, x_gender) is
    generated with both a same-gender and a different-gender partner, so the
    two conditions are matched pairs, not independent samples --
    test_paired_gap (McNemar) is the correct test, not test_group_gap
    (chi-square of independence)."""
    rows = []
    for lang in languages:
        pred_col = f"x_gender_{lang}"
        if pred_col not in df_subset.columns:
            continue
        sub = df_subset[df_subset[pred_col].notna()].copy()
        sub["correct"] = sub["x_gender"] == sub[pred_col]
        piv = sub.pivot_table(
            index=["sentence_id", "x_nom_sg", "x_gender"], columns="pairing", values="correct", aggfunc="first"
        ).dropna()
        result = test_paired_gap(piv["diff_gender"].tolist(), piv["same_gender"].tolist())
        result["language"] = lang
        result["model"] = model_name
        rows.append(result)
    return pd.DataFrame(rows)


def evaluate_model(df: pd.DataFrame, translation_cols: list[str], prediction_cols: list[str], model_name: str, output_dir: str) -> None:
    # "pairing" (same_gender/diff_gender), needed for the "romantic" scope
    # below -- study-specific derivation (x/y gold comparison), not
    # something the SDK can know about a generic dataset.
    df = df.copy()
    y_binary = df["y_gender"].isin(["MASCULINE", "FEMININE"])
    x_binary = df["x_gender"].isin(["MASCULINE", "FEMININE"])
    df["pairing"] = pd.NA
    df.loc[x_binary & y_binary & (df["x_gender"] == df["y_gender"]), "pairing"] = "same_gender"
    df.loc[x_binary & y_binary & (df["x_gender"] != df["y_gender"]), "pairing"] = "diff_gender"

    # DIVERSE gold (dey-pronoun/neopronoun forms, occurs in several sentence
    # styles) is a real, meaningful label, but the
    # non-binary axis is out of scope for this paper, so it's excluded from
    # every scope here.
    main_mask = x_binary
    scope_specs = [
        {"scope": "main", "mask": main_mask, "plot_dir": output_dir},
        *[
            {"scope": f"style_{s}", "sentence_style": s, "mask": main_mask & (df["sentence_style"] == s)}
            for s in (1, 2, 3, 4)
        ],
        {
            "scope": "names",
            "sentence_style": 6,
            "mask": main_mask & (df["sentence_style"] == 6),
            "group_col": "name_gender",
            "group_labels": {"n": "neutral", "MASCULINE": "masculine", "FEMININE": "feminine"},
        },
        {
            "scope": "romantic",
            "sentence_style": 5,
            "mask": df["pairing"].notna(),
            "group_col": "pairing",
            "group_labels": {"same_gender": "same_gender", "diff_gender": "diff_gender"},
        },
    ]
    error_rows = []
    for spec in scope_specs:
        spec = dict(spec)
        mask = spec.pop("mask")
        spec.setdefault("filename_prefix", f"{model_name}_")
        sub_ds = make_dataset(df[mask], translation_cols, prediction_cols)
        error_rows += ErrorAnalysis.grouped(sub_ds, "x_gender", **spec)

    error_df = pd.concat(error_rows, ignore_index=True)
    error_df.attrs["filename"] = f"{model_name}_error_analysis"
    save_dataframes(error_df, output_dir=output_dir)

    # Confusion matrix + logistic regression + stereotypicality: tied
    # specifically to "main" (every sentence style, DIVERSE excluded), since
    # that's where x_stereotypical (real-world occupation stereotypicality)
    # is a meaningful predictor.
    ds_main = make_dataset(df[main_mask], translation_cols, prediction_cols)
    cm_df = ConfusionMatrix(ds_main, "x_gender").analyze().T
    cm_df.attrs["filename"] = f"{model_name}_confusion_metrics"
    lr_df = format_significance_table(
        LogisticRegressionAnalysis(ds_main, "x_gender").analyze(predictor_col="x_stereotypical")
    )
    lr_df.attrs["filename"] = f"{model_name}_logistic_regression"
    save_dataframes(cm_df, lr_df, output_dir=output_dir)
    plot_stereotypicality(
        ds_main.df, "x_gender", "x_stereotypical", ds_main.prediction_columns,
        output_dir=output_dir, filename=f"{model_name}_stereotypicality.png",
    )

    # Significance tests (study-specific, not general SDK analyses). DIVERSE
    # gold excluded here too, same reasoning as main_mask above.
    names_df = df[df["sentence_style"] == 6]
    sig_neutral_df = format_significance_table(
        significance_neutral_names(
            names_df[(names_df["name_gender"] == "n") & x_binary[names_df.index]], LANGUAGES, model_name
        )
    )
    sig_neutral_df.attrs["filename"] = f"{model_name}_names_significance"
    romantic_df = df[df["pairing"].notna()]
    sig_hetero_df = format_significance_table(significance_heteronormativity(romantic_df, LANGUAGES, model_name))
    sig_hetero_df.attrs["filename"] = f"{model_name}_romantic_significance"
    save_dataframes(sig_neutral_df, sig_hetero_df, output_dir=output_dir)

    # Names composition plot (paper's figure 9): does an unambiguous name
    # change translation of a matching-form job, vs. a neutral name? Scoped
    # to the 4 name/job-gender pairs that actually occur in the dataset --
    # a curated slice for this one figure, not a standalone accuracy number
    # (that's what the "names" scope in error_analysis.csv is for).
    scenario_df = names_df[names_df["name_gender"].isin(["MASCULINE", "FEMININE", "n"]) & x_binary[names_df.index]]
    ds_names = make_dataset(scenario_df, translation_cols, prediction_cols)
    plot_gender_composition(
        [
            (f"{name.title() if name != 'n' else 'Neutral'} name\n+ {job.lower()}-form job",
             scenario_df[(scenario_df["name_gender"] == name) & (scenario_df["x_gender"] == job)], job)
            for name, job in (("MASCULINE", "MASCULINE"), ("FEMININE", "FEMININE"), ("n", "MASCULINE"), ("n", "FEMININE"))
        ],
        ds_names.prediction_columns,
        output_dir=output_dir,
        filename=f"{model_name}_names_gender_composition.png",
        suptitle="Does an unambiguous name change translation of a matching-form job,\ncompared to a neutral name?",
    )


def load_error_analysis(model: str) -> pd.DataFrame | None:
    path = os.path.join(OUTPUTS_ROOT, model, f"{model}_error_analysis.csv")
    return pd.read_csv(path) if os.path.exists(path) else None


def load_style_accuracy(model: str, style: int) -> dict[str, float] | None:
    df = load_error_analysis(model)
    if df is None:
        return None
    sub = df[df["sentence_style"] == style]
    if sub.empty:
        return None
    return dict(zip(sub["language"], sub["accuracy"].astype(float)))


def load_main_accuracy(model: str) -> dict[str, float] | None:
    df = load_error_analysis(model)
    if df is None:
        return None
    sub = df[df["scope"] == "main"]
    if sub.empty:
        return None
    return dict(zip(sub["language"], sub["accuracy"].astype(float)))


def build_style_comparison(models: list[str], style_a: int, style_b: int, label_a: str, label_b: str) -> pd.DataFrame:
    acc_a_by_model = {m: acc for m in models if (acc := load_style_accuracy(m, style_a)) is not None}
    acc_b_by_model = {m: acc for m in models if (acc := load_style_accuracy(m, style_b)) is not None}
    return compare_accuracy_by_language(acc_a_by_model, acc_b_by_model, label_a, label_b)


def build_hetero_significance_summary(models: list[str]) -> pd.DataFrame:
    frames = []
    for model in models:
        path = os.path.join(OUTPUTS_ROOT, model, f"{model}_romantic_significance.csv")
        if os.path.exists(path):
            frames.append(pd.read_csv(path))
    if not frames:
        return pd.DataFrame()
    return format_significance_table(pd.concat(frames, ignore_index=True))


def build_summary(models: list[str]) -> None:
    """Pure aggregation of the per-model CSVs `evaluate_model` already wrote
    -- no new computation, just reading them back and comparing across
    models/styles. Writes to study/outputs/summary/."""
    os.makedirs(SUMMARY_DIR, exist_ok=True)

    pronoun_df = build_style_comparison(models, 1, 2, "baseline", "pronoun")
    pronoun_df.to_csv(os.path.join(SUMMARY_DIR, "pronoun_effect_comparison.csv"), index=False)
    print("Saved pronoun_effect_comparison.csv")

    trans_df = build_style_comparison(models, 1, 3, "baseline", "trans")
    trans_pron_df = build_style_comparison(models, 2, 4, "baseline_pronoun", "trans_pronoun")
    trans_df.to_csv(os.path.join(SUMMARY_DIR, "trans_effect_comparison.csv"), index=False)
    trans_pron_df.to_csv(os.path.join(SUMMARY_DIR, "trans_effect_pronoun_comparison.csv"), index=False)
    print("Saved trans_effect_comparison.csv + trans_effect_pronoun_comparison.csv")

    main_accuracy = {m: acc for m in models if (acc := load_main_accuracy(m)) is not None}
    plot_accuracy_heatmap(
        main_accuracy,
        output_dir=SUMMARY_DIR,
        filename="accuracy_heatmap.png",
        title="Main-scope accuracy by system and language\n(all sentence styles pooled, masculine/feminine only)",
    )
    print("Saved accuracy_heatmap.png")

    hetero_sig_df = build_hetero_significance_summary(models)
    hetero_sig_df.to_csv(os.path.join(SUMMARY_DIR, "romantic_significance_summary.csv"), index=False)
    print("Saved romantic_significance_summary.csv")


if __name__ == "__main__":
    processed_dir = PROCESSED_DIR
    model_names = [
        f.replace("_processed.csv", "") for f in os.listdir(processed_dir) if f.endswith("_processed.csv")
    ]

    if not model_names:
        raise RuntimeError(f"No processed datasets found in '{processed_dir}'.")

    os.makedirs(OUTPUTS_ROOT, exist_ok=True)

    for model_name in model_names:
        print("\n" + "=" * 80)
        print(f"RUNNING ANALYSIS FOR MODEL: {model_name}")
        print("=" * 80)

        df, translation_cols, prediction_cols = load_processed_dataset(model_name, LANGUAGES)
        model_output_dir = os.path.join(OUTPUTS_ROOT, model_name)
        os.makedirs(model_output_dir, exist_ok=True)
        evaluate_model(df, translation_cols, prediction_cols, model_name, model_output_dir)

        print(f"[{model_name}] Analysis complete.")

    print("\n" + "=" * 80)
    print("BUILDING CROSS-MODEL SUMMARY")
    print("=" * 80)
    build_summary(model_names)
