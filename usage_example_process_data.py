import os
import pandas as pd
from Dataset import DEvalDataset
from analysis import ErrorAnalysis, ConfusionMatrix, LogisticRegressionAnalysis
from plots import (
    plot_error_analysis,
    plot_confusion_metrics,
    plot_logistic_regression,
    save_dataframes,
)

# -------------------------------
# Languages to analyze (extended)
# -------------------------------
LANGUAGES = ["es", "fr", "it", "no", "ar", "ru", "uk", "sv", "he"]

# -------------------------------
# Load processed dataset only, handle missing columns
# -------------------------------
def load_processed_dataset(model_name: str, languages: list[str]) -> DEvalDataset:
    processed_file = os.path.join("processed_data", f"{model_name}_processed.csv")

    if not os.path.exists(processed_file):
        raise FileNotFoundError(
            f"Processed dataset '{processed_file}' not found. This script does not rebuild datasets."
        )

    print(f"[{model_name}] Loading processed dataset from {processed_file}")

    df_columns = list(pd.read_csv(processed_file, nrows=0, sep=";").columns)

    available_translation_columns = [lang for lang in languages if lang in df_columns]
    available_prediction_columns = [lang for lang in languages if f"x_gender_{lang}" in df_columns]

    if not available_prediction_columns:
        raise RuntimeError(
            f"No x_gender columns found in '{processed_file}' for any of the requested languages."
        )

    print(f"[{model_name}] Available translation columns: {available_translation_columns}")
    print(f"[{model_name}] Available x_gender columns: {available_prediction_columns}")

    return (
        DEvalDataset.from_csv(
            processed_file,
            text_column="text",
            sep=";",
            translation_columns={lang: lang for lang in available_translation_columns},
            prediction_columns={lang: f"x_gender_{lang}" for lang in available_prediction_columns},
        ),
        available_prediction_columns,
    )


# -------------------------------
# Main analysis loop
# -------------------------------
if __name__ == "__main__":
    processed_dir = "processed_data"
    model_names = [
        f.replace("_processed.csv", "")
        for f in os.listdir(processed_dir)
        if f.endswith("_processed.csv")
    ]

    if not model_names:
        raise RuntimeError("No processed datasets found in 'processed_data/' folder.")

    outputs_root = "outputs"
    os.makedirs(outputs_root, exist_ok=True)

    for model_name in model_names:
        print("\n" + "=" * 80)
        print(f"RUNNING ANALYSIS FOR MODEL: {model_name}")
        print("=" * 80)

        ds, available_languages = load_processed_dataset(model_name, LANGUAGES)

        model_output_dir = os.path.join(outputs_root, model_name)
        os.makedirs(model_output_dir, exist_ok=True)

        # -------------------------------
        # 1. Error Analysis
        # -------------------------------
        error_df = ErrorAnalysis(ds, "x_gender").analyze().T
        error_df.attrs["filename"] = f"{model_name}_error_analysis"

        # -------------------------------
        # 2. Confusion Matrix
        # -------------------------------
        cm_df = ConfusionMatrix(ds, "x_gender").analyze().T
        cm_df.attrs["filename"] = f"{model_name}_confusion_metrics"

        # -------------------------------
        # 3. Logistic Regression
        # -------------------------------
        lr_results = LogisticRegressionAnalysis(ds, "x_gender").analyze(
            predictor_col="x_stereotypical"
        )
        lr_results.attrs["filename"] = f"{model_name}_logistic_regression"

        # -------------------------------
        # Save all analysis tables using your helper
        # -------------------------------
        save_dataframes(
            error_df,
            cm_df,
    #        lr_results,
            output_dir=model_output_dir,
        )

        # -------------------------------
        # Save plots
        # -------------------------------
        plot_error_analysis(
            error_df.T,
            output_dir=model_output_dir,
            filename=error_df.attrs["filename"],
        )
        plot_confusion_metrics(
            cm_df.T,
            output_dir=model_output_dir,
            filename=cm_df.attrs["filename"],
        )
        plot_logistic_regression(
            lr_results,
            output_dir=model_output_dir,
            filename=lr_results.attrs["filename"],
        )

        print(f"[{model_name}] Analysis complete. Languages processed: {available_languages}")
