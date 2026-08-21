"""Analysis driver for the romantic/name sentence styles (5 and 6) that are not
covered by usage_example_process_data.py (which only processes the main DEval
dataset, styles 1-4).

Reuses the existing ErrorAnalysis / ConfusionMatrix classes on two derived subsets
of processed_data/romantic_names/<model>_processed.csv:

- Neutral names (sentence_style == 6, name_gender == 'n'): does translation
  accuracy for the occupation noun collapse when the referring name gives no
  gender cue, and is the resulting error direction skewed toward one gender?
- Heteronormativity (sentence_style == 5): does accuracy for the occupation noun
  (grammatically unambiguous regardless of the partner's gender) differ between
  same-gender-coded and different-gender-coded romantic pairings?

No new translations or API calls - everything here reuses already-translated,
already-aligned data.
"""

import os
import pandas as pd

from Dataset import DEvalDataset
from analysis import ErrorAnalysis, ConfusionMatrix, test_direction_skew, test_paired_gap
from plots import plot_error_analysis, plot_confusion_metrics, save_dataframes

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
PROCESSED_DIR = "./processed_data/romantic_names"
OUTPUTS_ROOT = "./outputs"


def load_romantic_dataset(file_stub: str, languages: list[str]):
    processed_file = os.path.join(PROCESSED_DIR, f"{file_stub}_processed.csv")
    if not os.path.exists(processed_file):
        raise FileNotFoundError(
            f"Processed dataset '{processed_file}' not found. This script does not rebuild datasets."
        )

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
    """Binomial test per language: is the error direction (-> MASCULINE vs
    -> FEMININE) skewed away from the 50/50 expected under no systematic bias?"""
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
    """McNemar's test per language: does accuracy differ between same-gender-
    coded and different-gender-coded romantic pairings? Paired design: every
    subject sentence (sentence_id, x_nom_sg, x_gender) is generated with both
    a same-gender and a different-gender partner, so the two conditions are
    matched pairs, not independent samples -- test_paired_gap (McNemar) is
    the correct test, not test_group_gap (chi-square of independence)."""
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
        # column a = different-gender/hetero-coded, column b = same-gender-coded
        result = test_paired_gap(piv["diff_gender"].tolist(), piv["same_gender"].tolist())
        result["language"] = lang
        result["model"] = model_name
        rows.append(result)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    file_stubs = [
        f.replace("_processed.csv", "")
        for f in os.listdir(PROCESSED_DIR)
        if f.endswith("_processed.csv")
    ]

    if not file_stubs:
        raise RuntimeError(f"No processed datasets found in '{PROCESSED_DIR}'.")

    for file_stub in file_stubs:
        model_name = file_stub.replace("romantic_name_", "")
        print("\n" + "=" * 80)
        print(f"ROMANTIC/NAME ANALYSIS FOR MODEL: {model_name}")
        print("=" * 80)

        df, translation_cols, prediction_cols = load_romantic_dataset(file_stub, LANGUAGES)
        output_dir = os.path.join(OUTPUTS_ROOT, model_name, "romantic_names")
        os.makedirs(output_dir, exist_ok=True)

        # -------------------------------
        # 1.4 Neutral names (sentence_style 6, name_gender == 'n')
        # -------------------------------
        neutral_df = df[(df["sentence_style"] == 6) & (df["name_gender"] == "n")].copy()
        ds_neutral = make_dataset(neutral_df, translation_cols, prediction_cols)

        error_df = ErrorAnalysis(ds_neutral, "x_gender").analyze().T
        error_df.attrs["filename"] = f"{model_name}_neutral_names_error_analysis"

        cm_df = ConfusionMatrix(ds_neutral, "x_gender").analyze().T
        cm_df.attrs["filename"] = f"{model_name}_neutral_names_confusion_metrics"

        sig_neutral_df = significance_neutral_names(neutral_df, LANGUAGES, model_name)
        sig_neutral_df.attrs["filename"] = f"{model_name}_neutral_names_significance"

        save_dataframes(error_df, cm_df, sig_neutral_df, output_dir=output_dir)
        plot_error_analysis(error_df.T, output_dir=output_dir, filename=error_df.attrs["filename"])
        plot_confusion_metrics(cm_df.T, output_dir=output_dir, filename=cm_df.attrs["filename"])

        # -------------------------------
        # 1.6 Heteronormativity (sentence_style 5), binary x/y pairings only
        # -------------------------------
        romantic_df = df[df["sentence_style"] == 5].copy()
        binary_mask = romantic_df["x_gender"].isin(["MASCULINE", "FEMININE"]) & romantic_df["y_gender"].isin(
            ["MASCULINE", "FEMININE"]
        )
        romantic_df["pairing"] = pd.NA
        romantic_df.loc[binary_mask & (romantic_df["x_gender"] == romantic_df["y_gender"]), "pairing"] = "same_gender"
        romantic_df.loc[binary_mask & (romantic_df["x_gender"] != romantic_df["y_gender"]), "pairing"] = "diff_gender"

        romantic_binary_df = romantic_df[romantic_df["pairing"].notna()].copy()
        ds_romantic = make_dataset(romantic_binary_df, translation_cols, prediction_cols)

        for pairing_value in ("same_gender", "diff_gender"):
            err = (
                ErrorAnalysis(ds_romantic, "x_gender")
                .analyze(filter_col="pairing", filter_value=pairing_value)
                .T
            )
            err.attrs["filename"] = f"{model_name}_heteronormativity_error_analysis_{pairing_value}"
            save_dataframes(err, output_dir=output_dir)

        sig_hetero_df = significance_heteronormativity(romantic_binary_df, LANGUAGES, model_name)
        sig_hetero_df.attrs["filename"] = f"{model_name}_heteronormativity_significance"
        save_dataframes(sig_hetero_df, output_dir=output_dir)

        # Consistency check: DIVERSE-x recall within romantic sentences (should
        # be 0.0 everywhere, consistent with the main-dataset DIVERSE finding).
        diverse_df = romantic_df[romantic_df["x_gender"] == "DIVERSE"].copy()
        if len(diverse_df) > 0:
            ds_diverse = make_dataset(diverse_df, translation_cols, prediction_cols)
            diverse_cm = ConfusionMatrix(ds_diverse, "x_gender").analyze().T
            diverse_cm.attrs["filename"] = f"{model_name}_romantic_diverse_x_confusion_metrics"
            save_dataframes(diverse_cm, output_dir=output_dir)

        print(f"[{model_name}] Romantic/name analysis complete. Output: {output_dir}")
