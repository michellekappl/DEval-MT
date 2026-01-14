import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# -------------------------------
# Error Analysis Plot
# -------------------------------
def plot_error_analysis(df: pd.DataFrame, output_dir: str = "outputs", filename: str = "error_analysis.png"):
    """
    Plots a table of key metrics per language and error counts from a DataFrame
    returned by the analyze() method. Saves the figure to the specified output folder.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'language', 'accuracy', 'total', 'correct', 'error_count', and 'error_*'.
    output_dir (str): Folder to save the plot.
    filename (str): Name of the saved plot file.
    """
    if 'language' in df.columns:
        df = df.set_index('language')

    error_cols = [col for col in df.columns if isinstance(col, str) and col.startswith('error_')]
    df[error_cols] = df[error_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    error_data = df[error_cols].T.values
    languages = df.index.tolist()
    error_types = [col.replace('error_', '') for col in error_cols]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [1, 2]})

    # Table
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

    # Error counts
    max_val = np.max(error_data)
    im = ax2.imshow(error_data, cmap='Reds', aspect='auto', vmin=0, vmax=max_val)

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

    cbar = fig.colorbar(im, ax=ax2)
    cbar.set_label('Error Count')

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Logistic Regression Plot
# -------------------------------
def plot_logistic_regression(df: pd.DataFrame, output_dir: str = "outputs", filename: str = "logistic_regression_plot.jpg"):
    """
    Plots bar charts comparing logistic regression metrics for each language.

    Parameters:
    - df: DataFrame with columns ['language', 'coefficient', 'odds_ratio', 'p_value', 'ci_lower', 'ci_upper']
    - output_dir: folder to save plot
    - filename: plot filename
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

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Confusion Metrics Plot
# -------------------------------
def plot_confusion_metrics(df: pd.DataFrame, output_dir: str = "outputs", filename: str = "confusion_metrics.png"):
    """
    Plots confusion metrics (precision, recall, f1) for each language.
    Handles dynamic legend placement and prevents overlapping numbers on bars.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    languages = df["language"].tolist()
    metric_df = df.set_index("language")
    genders = sorted(set(col.split("_")[0] for col in metric_df.columns if "_precision" in col))
    metrics = ["precision", "recall", "f1_score"]

    fig, axes = plt.subplots(1, 3, figsize=(21, 6), sharey=True)

    for ax, metric in zip(axes, metrics):
        x = np.arange(len(genders))
        num_bars = len(languages)
        bar_width = min(0.8 / num_bars, 0.2)  # dynamic width to avoid overlap

        for i, lang in enumerate(languages):
            values = [metric_df.loc[lang, f"{gender}_{metric}"]
                      if f"{gender}_{metric}" in metric_df.columns else 0
                      for gender in genders]
            bars = ax.bar(x + i * bar_width, values, width=bar_width, label=lang)

            for bar, val in zip(bars, values):
                # Dynamic offset above bar
                offset = 0.01 + 0.02 * val
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    val + offset,
                    f"{val:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    rotation=0
                )

        ax.set_title(metric.title())
        ax.set_xticks(x + bar_width * (num_bars - 1) / 2)
        ax.set_xticklabels(genders, rotation=20, ha="right")  # prevent x-label overlap
        ax.set_ylim(0, 1.1)

    axes[0].set_ylabel("Score")

    # Dynamic legend inside figure
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=min(len(languages), 4),  # max 4 columns for readability
        frameon=False,
        fontsize=10,
        bbox_to_anchor=(0.5, 1.02)
    )

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')  # ensures nothing is cut off
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Save multiple DataFrames
# -------------------------------
def save_dataframes(*dfs, output_dir="outputs"):
    """
    Save any number of pandas DataFrames to CSV files in the given folder.
    Files will be named by their 'filename' attribute if present.
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, df in enumerate(dfs, start=1):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Argument {i} is not a pandas DataFrame")
        
        filename = df.attrs.get("filename", f"df_{i}")
        filepath = os.path.join(output_dir, f"{filename}.csv")
        df.to_csv(filepath, index=True)

    print(f"Saved {len(dfs)} CSV files to '{output_dir}/'")

def plot_combined_model_results(results_root="test_data/results", output_dir=None):
    """
    Automatically combines error analysis, confusion metrics, and logistic regression
    plots for all models in results_root folder.
    
    Saves combined plots into a `combined` folder inside results_root by default.
    
    Parameters:
    - results_root: folder containing per-model subfolders
    - output_dir: optional folder to save combined plots (default: results_root/combined)
    """
    if output_dir is None:
        output_dir = os.path.join(results_root, "combined")
    os.makedirs(output_dir, exist_ok=True)
    
    # Helper to gather model CSVs
    def gather_csvs(prefix):
        model_files = {}
        for model_name in os.listdir(results_root):
            model_path = os.path.join(results_root, model_name)
            if os.path.isdir(model_path):
                for fname in os.listdir(model_path):
                    if fname.startswith(prefix) and fname.endswith(".csv"):
                        model_files[model_name] = os.path.join(model_path, fname)
        return model_files
    
    # Helper to load CSVs into dict
    def load_dfs(file_dict):
        dfs = {}
        for model_name, path in file_dict.items():
            dfs[model_name] = pd.read_csv(path, sep=";")
        return dfs
    
    # ---------------------
    # 1. Error Analysis
    # ---------------------
    error_files = gather_csvs("error_analysis")
    if error_files:
        error_dfs = load_dfs(error_files)
        num_models = len(error_dfs)
        fig, axes = plt.subplots(num_models, 1, figsize=(14, 6*num_models))
        if num_models == 1:
            axes = [axes]
        
        for ax, (model_name, df) in zip(axes, error_dfs.items()):
            if 'language' in df.columns:
                df = df.set_index('language')
            error_cols = [c for c in df.columns if c.startswith('error_')]
            error_data = df[error_cols].T.values
            languages = df.index.tolist()
            error_types = [c.replace('error_', '') for c in error_cols]
            
            im = ax.imshow(error_data, cmap='Reds', aspect='auto')
            for i in range(error_data.shape[0]):
                for j in range(error_data.shape[1]):
                    ax.text(j, i, int(error_data[i, j]), ha='center', va='center', color='black')
            
            ax.set_xticks(np.arange(len(languages)))
            ax.set_xticklabels(languages)
            ax.set_yticks(np.arange(len(error_types)))
            ax.set_yticklabels(error_types)
            ax.set_title(f"{model_name} Error Counts")
            ax.set_xlabel("Language")
            ax.set_ylabel("Error Type")
            fig.colorbar(im, ax=ax)
        
        plt.tight_layout()
        error_out = os.path.join(output_dir, "combined_error_analysis.png")
        plt.savefig(error_out)
        plt.close()
        print("Saved combined error analysis:", error_out)
    
    # ---------------------
    # 2. Confusion Metrics
    # ---------------------
    cm_files = gather_csvs("confusion_matrix")
    if cm_files:
        cm_dfs = load_dfs(cm_files)
        num_models = len(cm_dfs)
        fig, axes = plt.subplots(num_models, 1, figsize=(21, 6*num_models), sharey=True)
        if num_models == 1:
            axes = [axes]
        
        for ax, (model_name, df) in zip(axes, cm_dfs.items()):
            languages = df["language"].tolist()
            metric_df = df.set_index("language")
            genders = sorted(set(col.split("_")[0] for col in metric_df.columns if "_precision" in col))
            metrics = ["precision", "recall", "f1_score"]
            
            for i, metric in enumerate(metrics):
                x = np.arange(len(genders))
                bar_width = 0.8 / len(languages)
                for j, lang in enumerate(languages):
                    values = [
                        metric_df.loc[lang, f"{gender}_{metric}"]
                        if f"{gender}_{metric}" in metric_df.columns else 0
                        for gender in genders
                    ]
                    bars = ax.bar(x + j*bar_width, values, width=bar_width, label=lang)
                    for bar, val in zip(bars, values):
                        ax.text(bar.get_x() + bar.get_width()/2, val+0.01, f"{val:.2f}",
                                ha="center", va="bottom", fontsize=9)
            ax.set_xticks(x + bar_width*(len(languages)-1)/2)
            ax.set_xticklabels(genders)
            ax.set_ylim(0, 1.1)
            ax.set_title(f"{model_name} Confusion Metrics")
        
        plt.tight_layout()
        cm_out = os.path.join(output_dir, "combined_confusion_metrics.png")
        plt.savefig(cm_out)
        plt.close()
        print("Saved combined confusion metrics:", cm_out)
    
    # ---------------------
    # 3. Logistic Regression
    # ---------------------
    lr_files = gather_csvs("logistic_regression")
    if lr_files:
        lr_dfs = load_dfs(lr_files)
        num_models = len(lr_dfs)
        metrics = ['coefficient', 'odds_ratio', 'p_value', 'ci_lower', 'ci_upper']
        fig, axes = plt.subplots(num_models, len(metrics), figsize=(4*len(metrics), 4*num_models))
        if num_models == 1:
            axes = [axes]
        
        for row_idx, (model_name, df) in enumerate(lr_dfs.items()):
            for col_idx, metric in enumerate(metrics):
                ax = axes[row_idx][col_idx] if num_models>1 else axes[col_idx]
                languages = df['language'].tolist()
                values = df[metric].tolist()
                ax.bar(languages, values, color='skyblue')
                ax.set_title(f"{model_name} {metric}")
                ax.set_ylabel(metric)
                ax.set_xticks(range(len(languages)))
                ax.set_xticklabels(languages)
        
        plt.tight_layout()
        lr_out = os.path.join(output_dir, "combined_logistic_regression.png")
        plt.savefig(lr_out)
        plt.close()
        print("Saved combined logistic regression:", lr_out)
