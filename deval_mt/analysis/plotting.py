import os
from typing import Mapping, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path
from statsmodels.nonparametric.smoothers_lowess import lowess

DEFAULT_GENDER_COLORS = {
    "MASCULINE": "tab:blue",
    "FEMININE": "tab:orange",
    "NEUTER": "tab:green",
    "DIVERSE": "tab:green",
    "UNKNOWN": "lightgrey",
}


# -------------------------------
# Error Analysis Plot
# -------------------------------
def plot_error_analysis(df: pd.DataFrame, output_dir: str = "outputs", filename: str = "error_analysis.png"):
    """
    Plots a table of key metrics per language and error counts from a DataFrame
    returned by ErrorAnalysis.analyze(). Saves the figure to the specified output folder.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'language', 'accuracy', 'total', 'correct', 'error_count', and 'error_*'.
    output_dir (str): Folder to save the plot.
    filename (str): Name of the saved plot file.
    """
    # --- normalize orientation ---
    # If error_* lives in the index instead of columns -> transpose
    has_error_cols = any(isinstance(c, str) and c.startswith("error_") for c in df.columns)
    has_error_idx = any(isinstance(i, str) and str(i).startswith("error_") for i in df.index)

    if (not has_error_cols) and has_error_idx:
        df = df.T

    # language as index (if present)
    if "language" in df.columns:
        df = df.set_index("language")

    # collect error_* columns
    error_cols = [col for col in df.columns if isinstance(col, str) and col.startswith("error_")]

    # --- HARD GUARD: no error_* columns -> skip ---
    if not error_cols:
        print(f"[plot_error_analysis] Skip '{filename}': no error_* columns found.")
        return

    # numeric + NaNs -> 0
    df[error_cols] = df[error_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    error_data = df[error_cols].T.to_numpy()

    # --- HARD GUARD: really empty -> skip ---
    if error_data.size == 0 or error_data.shape[0] == 0 or error_data.shape[1] == 0:
        print(f"[plot_error_analysis] Skip '{filename}': empty error_data shape={error_data.shape}")
        return

    # Drop error types that are structurally impossible for this data (e.g.
    # DIVERSE-related error types when the gold column was pre-filtered to
    # exclude DIVERSE) rather than showing rows that are guaranteed all-zero.
    nonzero_mask = (df[error_cols].to_numpy().sum(axis=0) > 0)
    error_cols = [c for c, keep in zip(error_cols, nonzero_mask) if keep]
    if not error_cols:
        print(f"[plot_error_analysis] Skip '{filename}': every error_* column is zero.")
        return
    error_data = df[error_cols].T.to_numpy()

    languages = df.index.tolist()
    error_types = [col.replace("error_", "") for col in error_cols]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={"height_ratios": [1, 2]})

    # Drop the constant "sentence_style" column from the table; show it in
    # the title instead if this call covers one specific style.
    style_values = df["sentence_style"].dropna().unique()
    style_note = f" (sentence_style={style_values[0]})" if len(style_values) == 1 else ""

    # Table
    table_data = df[["total", "correct", "accuracy", "true_error_count", "unknown_count"]].round(3)

    ax1.axis("off")
    if style_note:
        ax1.set_title(style_note.strip(" ()"), fontsize=10)
    table = ax1.table(
        cellText=table_data.values,
        rowLabels=table_data.index,
        colLabels=table_data.columns,
        cellLoc="center",
        rowLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Error counts
    max_val = np.nanmax(error_data)
    im = ax2.imshow(error_data, cmap="Reds", aspect="auto", vmin=0, vmax=max_val)

    for i in range(error_data.shape[0]):
        for j in range(error_data.shape[1]):
            ax2.text(j, i, int(error_data[i, j]), ha="center", va="center", color="black")

    ax2.set_xticks(np.arange(len(languages)))
    ax2.set_xticklabels(languages)
    ax2.set_yticks(np.arange(len(error_types)))
    ax2.set_yticklabels(error_types)
    ax2.set_xlabel("Language")
    ax2.set_ylabel("Error Type")
    ax2.set_title("Error Counts")

    cbar = fig.colorbar(im, ax=ax2)
    cbar.set_label("Error Count")

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Significance table: adds a significance-star column to a result table.
# -------------------------------
def format_significance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'significance' column (*/**/*** on p_value) to any result with
    a 'p_value' column -- e.g. LogisticRegressionAnalysis.analyze(),
    test_paired_gap(), or test_group_gap() results. The same star convention
    used for the paper's tables (*** p<0.001, ** p<0.01, * p<0.05)."""

    def _stars(p):
        return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""

    out = df.copy()
    out["significance"] = out["p_value"].apply(_stars)
    return out


# -------------------------------
# Confusion flow (Sankey-style ribbon diagram): where does each gold gender
# end up after translation, per language.
# -------------------------------
def _sankey_positions(totals, order, total, avail, gap):
    pos = {}
    y = 1.0
    for k in order:
        h = totals[k] / total * avail
        pos[k] = (y - h, y)
        y -= h + gap
    return pos


def _draw_sankey_panel(ax, flows, gold_order, pred_order, node_colors, box_w=0.05, gap=0.03):
    total = sum(flows.values())
    if total == 0:
        ax.axis("off")
        return
    avail = 1 - gap * (len(pred_order) - 1)  # same scale on both sides -> ribbons don't taper
    left_totals = {g: sum(flows.get((g, p), 0) for p in pred_order) for g in gold_order}
    right_totals = {p: sum(flows.get((g, p), 0) for g in gold_order) for p in pred_order}
    left_pos = _sankey_positions(left_totals, gold_order, total, avail, gap)
    right_pos = _sankey_positions(right_totals, pred_order, total, avail, gap)

    for g in gold_order:
        b, t = left_pos[g]
        ax.add_patch(Rectangle((0, b), box_w, t - b, color=node_colors[g], zorder=3))
    for p in pred_order:
        b, t = right_pos[p]
        ax.add_patch(Rectangle((1 - box_w, b), box_w, t - b, color=node_colors[p], zorder=3))

    left_cursor = {g: left_pos[g][1] for g in gold_order}
    right_cursor = {p: right_pos[p][1] for p in pred_order}
    for g in gold_order:
        for p in pred_order:
            v = flows.get((g, p), 0)
            if v == 0:
                continue
            h = v / total * avail
            lt, lb = left_cursor[g], left_cursor[g] - h
            rt, rb = right_cursor[p], right_cursor[p] - h
            left_cursor[g] -= h
            right_cursor[p] -= h
            xm1, xm2 = box_w + (1 - 2 * box_w) * 0.4, box_w + (1 - 2 * box_w) * 0.6
            verts = [
                (box_w, lt), (xm1, lt), (xm2, rt), (1 - box_w, rt),
                (1 - box_w, rb), (xm2, rb), (xm1, lb), (box_w, lb),
                (box_w, lt),
            ]
            codes = [
                Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.CLOSEPOLY,
            ]
            ax.add_patch(PathPatch(Path(verts, codes), facecolor=node_colors[g], edgecolor="none", alpha=0.5, zorder=2))

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")


def plot_confusion_flow(
    df: pd.DataFrame,
    gold_col: str,
    prediction_columns: Mapping[str, str],
    output_dir: str = "outputs",
    filename: str = "confusion_flow.png",
    gender_colors: Optional[Mapping[str, str]] = None,
):
    """One gold -> predicted flow panel (Sankey-style ribbon diagram) per
    language in `prediction_columns`, in a single figure.

    Parameters
    ----------
    df : pd.DataFrame
        Rows with a gold-label column and one prediction column per language.
    gold_col : str
        Column holding the gold `Gender` name.
    prediction_columns : {language: column_name}
        Same shape as `DEvalDataset.prediction_columns`.
    gender_colors : {Gender name: matplotlib color}, optional
        Defaults to `DEFAULT_GENDER_COLORS`.
    """
    colors = dict(DEFAULT_GENDER_COLORS)
    if gender_colors:
        colors.update(gender_colors)

    gold_values = [g for g in colors if g != "UNKNOWN" and g in set(df[gold_col].dropna())]
    if not gold_values:
        print(f"[plot_confusion_flow] Skip '{filename}': no known gold values in '{gold_col}'.")
        return

    languages = [lang for lang, col in prediction_columns.items() if col in df.columns]
    if not languages:
        print(f"[plot_confusion_flow] Skip '{filename}': none of the prediction_columns are present.")
        return

    fig, axes = plt.subplots(1, len(languages), figsize=(2.1 * len(languages), 3.4))
    if len(languages) == 1:
        axes = [axes]

    for ax, lang in zip(axes, languages):
        col = prediction_columns[lang]
        sub = df[df[gold_col].isin(gold_values) & df[col].notna()]
        pred_values = gold_values + (["UNKNOWN"] if (sub[col] == "UNKNOWN").any() else [])
        flows = {}
        wrong_by_gold = {g: 0 for g in gold_values}
        total_by_gold = {g: 0 for g in gold_values}
        for gold, pred in zip(sub[gold_col], sub[col]):
            # Analyzers can never predict DIVERSE directly (no morphological
            # marker for it) -- NEUTER is the closest achievable signal, so
            # DIVERSE gold + NEUTER pred is drawn as a match, not a DIVERSE
            # -> UNKNOWN ribbon (matches ErrorAnalysis's correctness rule).
            if gold == "DIVERSE" and pred == "NEUTER":
                pred_bucket = "DIVERSE"
            else:
                pred_bucket = pred if pred in gold_values else "UNKNOWN"
                wrong_by_gold[gold] += pred != gold
            total_by_gold[gold] += 1
            flows[(gold, pred_bucket)] = flows.get((gold, pred_bucket), 0) + 1
        _draw_sankey_panel(ax, flows, gold_values, pred_values, colors)
        # Per-gold error rate (1 - recall), e.g. "fem 4% / masc 6%".
        error_rates = " / ".join(
            f"{g.lower()[:4]} {wrong_by_gold[g] / total_by_gold[g] * 100:.0f}%"
            for g in gold_values
            if total_by_gold[g] > 0
        )
        ax.set_title(f"{lang}\n{error_rates}", fontsize=8.5)

    axes[0].text(-0.05, 1.14, "gold", fontsize=7, ha="left", transform=axes[0].transAxes, color="grey")
    axes[0].text(1.0, 1.14, "pred", fontsize=7, ha="right", transform=axes[0].transAxes, color="grey")

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[g], label=g.lower()) for g in gold_values]
    fig.legend(handles=legend_handles, loc="lower center", ncol=len(gold_values), fontsize=8.5, bbox_to_anchor=(0.5, -0.05), frameon=False)
    fig.suptitle("Where does each gold gender end up, per language?", fontsize=10.5)

    plt.tight_layout(rect=[0, 0.08, 1, 0.9])
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Gender composition: for a scenario already narrowed down to one expected
# answer (e.g. one gold value, or a name/job-gender combination), what
# fraction of predictions actually land in each gender bucket, per language.
# One stacked bar per scenario, several scenarios side by side in one
# figure -- e.g. "masculine name + masculine-form job" vs. "neutral name +
# masculine-form job", so a name's presence/gender can be compared directly.
# -------------------------------
def plot_gender_composition(
    scenarios: list,
    prediction_columns: Mapping[str, str],
    output_dir: str = "outputs",
    filename: str = "gender_composition.png",
    gender_colors: Optional[Mapping[str, str]] = None,
    suptitle: Optional[str] = None,
    ncols: Optional[int] = None,
):
    """One stacked bar chart per scenario, arranged in a grid in a single
    figure -- matches the paper's own figure 8/9 layout (e.g. a 2x2 grid of
    name/job-gender combinations) rather than a single row.

    Parameters
    ----------
    scenarios : list of (title, df, correct_bucket)
        `df` is a DataFrame already filtered to that scenario (e.g. one gold
        value, or one name-gender + job-gender combination). `correct_bucket`
        is the prediction bucket ("MASCULINE"/"FEMININE"/"NEUTER"/"UNKNOWN")
        that counts as correct for this scenario -- e.g. "NEUTER" for a
        DIVERSE-gold scenario, since analyzers can't predict DIVERSE
        directly. Drawn at the bottom of the stack.
    prediction_columns : {language: column_name}
        Same shape as `DEvalDataset.prediction_columns`.
    ncols : int | None
        Panels per row. Defaults to a near-square grid (e.g. 4 scenarios ->
        2x2, matching the paper's figure 9).
    """
    colors = {
        "MASCULINE": DEFAULT_GENDER_COLORS["MASCULINE"],
        "FEMININE": DEFAULT_GENDER_COLORS["FEMININE"],
        "NEUTER": DEFAULT_GENDER_COLORS["NEUTER"],
        "UNKNOWN": DEFAULT_GENDER_COLORS["UNKNOWN"],
    }
    if gender_colors:
        colors.update(gender_colors)
    buckets = ["MASCULINE", "FEMININE", "NEUTER", "UNKNOWN"]

    languages = list(prediction_columns.keys())
    n = len(scenarios)
    if ncols is None:
        ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(3.4 * ncols, 3.0 * nrows), sharey=True, squeeze=False)
    flat_axes = axes.flatten()

    for ax, (title, sub_df, correct_bucket) in zip(flat_axes, scenarios):
        stack_order = [correct_bucket] + [b for b in buckets if b != correct_bucket]
        counts_by_lang = {lang: {b: 0 for b in buckets} for lang in languages}
        for lang in languages:
            col = prediction_columns[lang]
            if col not in sub_df.columns:
                continue
            for pred, count in sub_df[col].value_counts().items():
                bucket = pred if pred in counts_by_lang[lang] else "UNKNOWN"
                counts_by_lang[lang][bucket] += count

        bottoms = np.zeros(len(languages))
        for bucket in stack_order:
            vals = [
                counts_by_lang[lang][bucket] / (sum(counts_by_lang[lang].values()) or 1) * 100
                for lang in languages
            ]
            ax.bar(languages, vals, bottom=bottoms, color=colors[bucket])
            bottoms += np.array(vals)

        ax.set_title(title, fontsize=8.5)
        ax.tick_params(labelsize=7.5)

    for ax in flat_axes[n:]:
        ax.axis("off")
    for row in range(nrows):
        flat_axes[row * ncols].set_ylabel("% of predictions", fontsize=8)

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[b], label=b.title()) for b in buckets]
    flat_axes[min(ncols, n) - 1].legend(
        handles=legend_handles, fontsize=7, loc="upper left", bbox_to_anchor=(1.0, 1.0),
        title="Predicted", title_fontsize=7.5,
    )
    if suptitle:
        fig.suptitle(suptitle, fontsize=9.5)

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Stereotypicality: accuracy vs. how stereotype-congruent an instance is.
# Per-instance (predictor, correct) pairs pooled across languages,
# LOWESS-smoothed (it=0 -- see note below) rather than binned.
# -------------------------------
def plot_stereotypicality(
    df: pd.DataFrame,
    gold_col: str,
    predictor_col: str,
    prediction_columns: Mapping[str, str],
    output_dir: str = "outputs",
    filename: str = "stereotypicality.png",
    frac: float = 0.3,
):
    """LOWESS-smoothed accuracy vs. `predictor_col`, pooled over every
    language in `prediction_columns`.

    `it=0` (no robustifying iterations) is used deliberately: with `it=1`,
    LOWESS's iterative reweighting treats the minority class (translation
    errors, usually a small share of predictions) as "outliers" and
    downweights it further each iteration, inflating the curve toward 100%
    at the edges where there's less data to stabilize the fit.
    """
    languages = [lang for lang, col in prediction_columns.items() if col in df.columns]
    if not languages or predictor_col not in df.columns:
        print(f"[plot_stereotypicality] Skip '{filename}': missing predictor_col or prediction columns.")
        return

    xs, ys = [], []
    for lang in languages:
        col = prediction_columns[lang]
        sub = df[df[col].notna()]
        is_correct = sub[gold_col] == sub[col]
        xs.extend(sub[predictor_col].tolist())
        ys.extend((is_correct.astype(float) * 100).tolist())

    if len(xs) < 2:
        print(f"[plot_stereotypicality] Skip '{filename}': not enough data points.")
        return

    smoothed = lowess(ys, xs, frac=frac, it=0, return_sorted=True)

    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.plot(smoothed[:, 0], smoothed[:, 1], color="tab:red", lw=2.0)
    ax.set_xlabel(predictor_col, fontsize=7.5)
    ax.set_ylabel("Translation accuracy (%)", fontsize=7.5)
    ax.tick_params(labelsize=7)
    ax.set_title(f"Accuracy vs. '{predictor_col}'", fontsize=8.5)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()
    print("Saved:", filepath)


# -------------------------------
# Accuracy heatmap: one cell per (group, language), e.g. system x language.
# Same shape as compare_accuracy_by_language's inputs, so results from that
# function's callers can feed straight into this one.
# -------------------------------
def plot_accuracy_heatmap(
    accuracies: Mapping[str, Mapping[str, float]],
    output_dir: str = "outputs",
    filename: str = "accuracy_heatmap.png",
    title: str = "Accuracy by group and language",
    group_labels: Optional[Mapping[str, str]] = None,
):
    """Heatmap of accuracy (%) with one row per group (e.g. system/model)
    and one column per language.

    Parameters
    ----------
    accuracies : {group: {language: accuracy}}
        Accuracy as a 0-1 fraction (converted to % for display). Same shape
        `compare_accuracy_by_language` takes as input.
    group_labels : {raw_key: display_label}, optional
        Relabels rows for display (e.g. "gpt-4o" -> "GPT-4o") without
        touching the `accuracies` keys themselves.
    """
    groups = list(accuracies.keys())
    languages = sorted({lang for langs in accuracies.values() for lang in langs})
    if not groups or not languages:
        print(f"[plot_accuracy_heatmap] Skip '{filename}': no data.")
        return

    data = np.full((len(groups), len(languages)), np.nan)
    for i, group in enumerate(groups):
        for j, lang in enumerate(languages):
            if lang in accuracies[group]:
                data[i, j] = accuracies[group][lang] * 100

    fig, ax = plt.subplots(figsize=(1.1 * len(languages) + 2, 0.5 * len(groups) + 1.5))
    # viridis instead of a red-green diverging map: colorblind-safe and
    # perceptually uniform.
    im = ax.imshow(data, cmap="viridis", vmin=30, vmax=100, aspect="auto")

    ax.set_xticks(range(len(languages)))
    ax.set_xticklabels(languages)
    ax.set_yticks(range(len(groups)))
    ax.set_yticklabels([group_labels.get(g, g) if group_labels else g for g in groups])

    for i in range(len(groups)):
        for j in range(len(languages)):
            if np.isnan(data[i, j]):
                continue
            text_color = "white" if data[i, j] < 65 else "black"
            ax.text(j, i, f"{data[i, j]:.0f}", ha="center", va="center", fontsize=8, color=text_color)

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label("Accuracy (%)")
    ax.set_title(title, fontsize=10)

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches="tight")
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
