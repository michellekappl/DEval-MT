#this module has the functions to plot the output and save them into csv files.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_error_analysis(df: pd.DataFrame, filename: str = "error_analysis.png"):
    """
    Plots a table of key metrics per language and error counts from a DataFrame
    returned by the analyze() method. Saves the figure to outputs folder.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'language', 'accuracy', 'total', 'correct', 'error_count', and 'error_*'.
    filename (str): Name of the saved plot file.
    """
    # Set language as index if needed
    if 'language' in df.columns:
        df = df.set_index('language')

    # Select all error columns where the column name is a string
    error_cols = [col for col in df.columns if isinstance(col, str) and col.startswith('error_')]

    # Convert error columns to numeric
    df[error_cols] = df[error_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Create outputs folder if it does not exist
    os.makedirs('outputs', exist_ok=True)
    filepath = os.path.join('outputs', filename)

    # Prepare error counts data
    error_data = df[error_cols].T.values  # rows = error types, columns = languages
    languages = df.index.tolist()
    error_types = [col.replace('error_', '') for col in error_cols]

    # Create figure with two subplots (top: table, bottom: error counts)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [1, 2]})

    # Top: Table of key metrics
    table_data = df[['total', 'correct', 'accuracy', 'error_count']].round(3)
    ax1.axis('off')
    table = ax1.table(cellText=table_data.values,
                      rowLabels=table_data.index,
                      colLabels=table_data.columns,
                      cellLoc='center',
                      rowLoc='center',
                      loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    ax1.set_title('Language Metrics Table')

    # Bottom: Error counts
    # Use normalized colormap to reduce dominance of high values
    max_val = np.max(error_data)

    im = ax2.imshow(error_data, cmap='Reds', aspect='auto', vmin=0, vmax=max_val)

    # Annotate cells with values
    for i in range(error_data.shape[0]):
        for j in range(error_data.shape[1]):
            ax2.text(j, i, int(error_data[i, j]), ha='center', va='center', color='black')

    ax2.set_xticks(np.arange(len(languages)))
    ax2.set_xticklabels(languages)
    ax2.set_yticks(np.arange(len(error_types)))
    ax2.set_yticklabels(error_types)
    ax2.set_xlabel('Language')
    ax2.set_ylabel('Error Type')
    ax2.set_title('Error Counts')

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax2)
    cbar.set_label('Error Count')

    plt.tight_layout()
    plt.savefig(filepath)
    #plt.show()
    plt.close()
    print(f"Plot saved to {filepath}")


def plot_logistic_regression(df: pd.DataFrame, folder="outputs"):
    """
    Plots bar charts comparing logistic regression metrics for each language.

    Parameters:
    - df: DataFrame with columns ['language', 'coefficient', 'odds_ratio', 'p_value', 'ci_lower', 'ci_upper']
    """
    metrics = ['coefficient', 'odds_ratio', 'p_value', 'ci_lower', 'ci_upper']
    colors = ['skyblue', 'salmon']
    languages = df['language'].tolist()

    fig, axes = plt.subplots(1, len(metrics), figsize=(14, 4))

    for i, metric in enumerate(metrics):
        values = df[metric].tolist()
        axes[i].bar(languages, values, color=colors)
        axes[i].set_title(f'{metric.capitalize()} Comparison')
        axes[i].set_ylabel(metric.capitalize())
        axes[i].set_xticks(range(len(languages)))
        axes[i].set_xticklabels(languages)
        axes[i].grid(True, axis='y')

    plt.suptitle('Logistic Regression Metrics by Language')
    plt.tight_layout()
    filename = "logistic_regression_plot"
    filepath = f"{folder}/{filename}.jpg"
    os.makedirs(folder, exist_ok=True)
    plt.savefig(filepath)
    #plt.show()


def save_dataframes(*dfs, filenames='', folder="outputs"):
    """
    Save any number of pandas DataFrames to CSV files in the given folder.
    Files will be named df_1.csv, df_2.csv, df_3.csv, ...
    """
    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    for i, df in enumerate(dfs, start=1):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Argument {i} is not a pandas DataFrame")
        
        if not df.attrs.get("filename"):
            filename = f"{folder}/df_{i}.csv"
            df.to_csv(filename, index=True)
        else:
            filename = df.attrs.get("filename")
            filepath = f"{folder}/{filename}.csv"
            df.to_csv(filepath, index=True)
        #print(filepath)

    print(f"Saved {len(dfs)} CSV files to '{folder}/'")


def plot_confusion_matrix(df: pd.DataFrame, filename="confusion_metrics.png"):
    import os
    import numpy as np
    import matplotlib.pyplot as plt

    os.makedirs("outputs", exist_ok=True)

    languages = df["language"].tolist()
    metric_df = df.set_index("language")

    genders = sorted(set(col.split("_")[0] for col in metric_df.columns if "_precision" in col))
    metrics = ["precision", "recall", "f1_score"]

    fig, axes = plt.subplots(1, 3, figsize=(21, 6), sharey=True)

    for ax, metric in zip(axes, metrics):
        x = np.arange(len(genders))
        bar_width = 0.8 / len(languages)

        for i, lang in enumerate(languages):
            values = [
                metric_df.loc[lang, f"{gender}_{metric}"]
                if f"{gender}_{metric}" in metric_df.columns else 0
                for gender in genders
            ]

            bars = ax.bar(
                x + i * bar_width,
                values,
                width=bar_width,
                label=lang
            )

            # Add numeric value on top of each bar
            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    val + 0.01,
                    f"{val:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9
                )

        ax.set_title(metric.title())
        ax.set_xticks(x + bar_width * (len(languages) - 1) / 2)
        ax.set_xticklabels(genders)
        ax.set_ylim(0, 1.1)

    axes[0].set_ylabel("Score")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(languages), bbox_to_anchor=(0.5, -0.07))

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    save_path = os.path.join("outputs", filename)
    plt.savefig(save_path)
    plt.close()

    print("Saved:", save_path)
