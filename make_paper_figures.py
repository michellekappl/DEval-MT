"""Generates the 5 compact paper figures from already-existing outputs/ and
processed_data/. No new experiments, only aggregation + plotting.

Figures (see plan for the reasoning behind this set):
1. Accuracy heatmap (6 systems x 7 languages), replaces the big 1.1 table.
2. Occupation-level bias scatter (real-world vs. translated gender distribution),
   adapted from the bachelor-thesis version (mt_gender_german/statistics.ipynb).
3. Context-effect dumbbell chart, combining 1.3 (trans) and 1.5 (pronoun).
4. Diverging bars for 1.4 (neutral names) + 1.6 (heteronormativity), pooled
   across systems with significance stars from analysis/significance.py.
5. Forest plot for 1.7 (stereotypicality regression, GPT-4o).

Run from the DEval-MT repo root.
"""

import ast
import csv
import glob
import hashlib
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from statsmodels.nonparametric.smoothers_lowess import lowess

from Dataset import DEvalDataset
from analysis import ErrorAnalysis, LogisticRegressionAnalysis
from analysis.significance import test_direction_skew, test_group_gap, test_paired_gap

OUTPUT_DIR = "/Users/michellekappl/Work/Wissenschaft/gebnlp_2026/paper/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_binary_dataset(model: str, styles=(1, 2, 3, 4)) -> DEvalDataset:
    """Main-dataset loader for the "general" figures (1, 3, 5, logistic
    regression table) -- restricted to sentence styles 1-4 AND to gold
    x_gender in {MASCULINE, FEMININE}. DIVERSE (dey-pronoun) instances are
    deliberately excluded here: they're out of scope for these pooled/
    aggregate views and are handled in their own dedicated figures
    (7, 7b, and the names figures) instead, where mixing them in would
    quietly bias the pooled binary-gender numbers with a class that
    behaves completely differently (~0-2% recall vs. 80-90%+ for M/F)."""
    processed_file = f"processed_data/avg_DEval/{model}_processed.csv"
    df = pd.read_csv(processed_file, sep=";")
    df = df[df["sentence_style"].isin(styles) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
    translation_columns = {lang: lang for lang in LANGUAGES if lang in df.columns}
    prediction_columns = {
        lang: f"x_gender_{lang}" for lang in LANGUAGES if f"x_gender_{lang}" in df.columns
    }
    ds = DEvalDataset(df, text_column="text")
    ds.translation_columns = translation_columns
    ds.prediction_columns = prediction_columns
    return ds

LANGUAGES = ["es", "fr", "it", "ar", "ru", "uk", "he"]
MODELS = ["google", "google_llm", "deepl", "microsoft", "systran", "gpt-4o"]
# Shared gender color scheme, used across every bar/stacked-bar figure so the
# same category always has the same color (previously feminine was tab:red
# in figs 4/7/8 but the +pronoun/+trans figure (3) used tab:blue/tab:orange
# for an unrelated dimension -- inconsistent across the paper, and red+green
# together (figs 7/8) is also a red-green colorblindness clash). Orange
# instead of red for feminine avoids that clash and matches figure 3's palette.
GENDER_COLORS = {
    "masculine": "tab:blue",
    "feminine": "tab:orange",
    "diverse": "tab:green",
    "neuter": "tab:green",
    "unknown": "lightgrey",
}
MODEL_LABELS = {
    "google": "Google",
    "google_llm": "Google LLM",
    "deepl": "DeepL",
    "microsoft": "Microsoft",
    "systran": "SYSTRAN",
    "gpt-4o": "GPT-4o",
}


# ---------------------------------------------------------------------------
# Figure 1: accuracy heatmap
# ---------------------------------------------------------------------------
def figure_1_accuracy_heatmap():
    # Recomputed directly (not from outputs/*_error_analysis.csv) using
    # load_binary_dataset: the precomputed CSV pools DIVERSE gold instances
    # in with MASCULINE/FEMININE, which is now deliberately out of scope here.
    data = np.zeros((len(MODELS), len(LANGUAGES)))
    for i, model in enumerate(MODELS):
        ds = load_binary_dataset(model)
        error_df = ErrorAnalysis(ds, "x_gender").analyze(analyze_error_patterns=False)
        for j, lang in enumerate(LANGUAGES):
            row = error_df[error_df["language"] == lang]
            data[i, j] = float(row["accuracy"].iloc[0]) * 100 if not row.empty else np.nan

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    # viridis instead of RdYlGn: colorblind-safe (RdYlGn is a red-green
    # diverging map, unreadable for the ~8% of men with red-green color
    # vision deficiency) and perceptually uniform.
    im = ax.imshow(data, cmap="viridis", vmin=30, vmax=100, aspect="auto")

    ax.set_xticks(range(len(LANGUAGES)))
    ax.set_xticklabels(LANGUAGES)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([MODEL_LABELS[m] for m in MODELS])

    for i in range(len(MODELS)):
        for j in range(len(LANGUAGES)):
            # White text on viridis's dark purple/blue low end, black text
            # on its light yellow/green high end -- fixed dark text (fine
            # for RdYlGn's pale mid-tones) was unreadable on viridis's dark end.
            text_color = "white" if data[i, j] < 65 else "black"
            ax.text(
                j, i, f"{data[i, j]:.0f}", ha="center", va="center", fontsize=8, color=text_color
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label("Accuracy (%)")
    # Explicitly states which sentence styles are pooled here, so the figure
    # is self-contained without needing the caption text to clarify it.
    ax.set_title(
        "Main-dataset accuracy by system and language\n(sentence styles 1-4 pooled, masculine/feminine only)",
        fontsize=10,
    )
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig1_accuracy_heatmap.pdf")
    plt.savefig(path)
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 2: occupation-level bias scatter
# ---------------------------------------------------------------------------
# English labels for the 36 KldB 2-digit "Berufshauptgruppe" groups, keyed
# by their 2-digit code (independent of the German name in decoder.csv, which
# can change wording slightly between exports).
FINE_CATEGORY_EN = {
    "11": "Agriculture, Animal Husbandry, Forestry",
    "12": "Horticulture, Floristry",
    "21": "Raw Material Extraction, Glass & Ceramics Processing",
    "22": "Plastics & Wood Production/Processing",
    "23": "Paper & Printing, Technical Media Design",
    "24": "Metal Production, Processing & Construction",
    "25": "Machinery & Automotive Technology",
    "26": "Mechatronics, Energy & Electrical",
    "27": "Technical Development, Design & Production Control",
    "28": "Textiles & Leather",
    "29": "Food Production & Processing",
    "31": "Construction Planning, Architecture, Surveying",
    "32": "Building & Civil Engineering Construction",
    "33": "Interior Fitting/Finishing",
    "34": "Building & Utilities Engineering",
    "41": "Mathematics, Biology, Chemistry, Physics",
    "42": "Geology, Geography, Environmental Protection",
    "43": "Computer Science & Other ICT",
    "51": "Transport, Logistics (excl. Vehicle Operation)",
    "52": "Vehicle & Transport Equipment Operation",
    "53": "Protection, Security, Surveillance",
    "54": "Cleaning",
    "61": "Purchasing, Sales & Trade",
    "62": "Retail Sales",
    "63": "Tourism, Hotel & Restaurant",
    "71": "Business Management & Organization",
    "72": "Financial Services, Accounting, Tax Consulting",
    "73": "Law & Administration",
    "81": "Medical & Health Care",
    "82": "Non-Medical Health, Personal Care, Medical Technology",
    "83": "Education, Social Work, Home Economics, Theology",
    "84": "Teaching & Training",
    "91": "Humanities, Social & Economic Sciences",
    "92": "Advertising, Marketing, Commercial & Editorial Media",
    "93": "Product Design, Crafts",
    "94": "Performing & Entertainment Arts",
}


def load_code_to_category():
    """Map each 3-digit occupation code to its 2-digit "Berufshauptgruppe"
    prefix (KldB 2010 hierarchy, names from utilities/decoder.csv). This is
    the middle granularity between the 140 3-digit codes (too few source
    sentences per point, ~4-28, noisy/pinned at 0%/100%) and the 9 broad
    main_branchen categories (too sparse, only 54 points total). 36 groups,
    min. 24 source sentences per group."""
    code_to_cat = {}
    with open("processed_data/avg_DEval/google_processed.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            code = str(row["x_group"])
            if len(code) >= 2:
                code_to_cat[code] = code[:2]

    cat_names = {}
    with open(
        "create_deval_synth/job_statistics/utilities/decoder.csv", newline="", encoding="utf-8"
    ) as f:
        for row in csv.DictReader(f, delimiter=";"):
            code = row["Code"].strip()
            if len(code) == 2:
                cat_names[code] = FINE_CATEGORY_EN.get(code, row["Bezeichnung"])
    return code_to_cat, cat_names


# Short English labels for the 9 broad main_branchen ("Berufsbereich")
# categories, keyed by the German names as they appear in main_branchen.csv.
# Kept short (2-4 words) so the legend stays compact without dropping any
# of the 9 categories.
BROAD_CATEGORY_EN = {
    "Militär": "Military",
    "Land-, Forst-, Tierwirtschaft, Gartenbau": "Agriculture & Forestry",
    "Rohstoffgewinnung, Produktion, Fertigung": "Manufacturing",
    "Bau,Architektur,Vermessung,Gebäudetechn.": "Construction & Architecture",
    "Naturwissenschaft, Geografie, Informatik": "Science & IT",
    "Verkehr, Logistik, Schutz und Sicherheit": "Transport & Security",
    "Kaufm.Dienstl.,Handel,Vertrieb,Tourismus": "Trade & Tourism",
    "Unternehmensorga,Buchhalt,Recht,Verwalt.": "Business & Law",
    "Gesundheit, Soziales, Lehre u. Erziehung": "Health & Education",
    "Geisteswissenschaften, Kultur,Gestaltung": "Humanities & Culture",
}


def load_code_to_broad_category():
    """Map each 3-digit occupation code to one of the 9 broad main_branchen
    categories (1-digit KldB "Berufsbereich") -- the coarsest useful level."""
    code_to_cat = {}
    cat_names = {}
    with open(
        "create_deval_synth/job_statistics/main_branchen.csv", newline="", encoding="utf-8"
    ) as f:
        for row in csv.DictReader(f, delimiter=";"):
            cat = row["Code"]
            cat_names[cat] = BROAD_CATEGORY_EN.get(row["main_branche"], row["main_branche"])
            try:
                jobs = ast.literal_eval(row["corresponding_jobs"])
            except (ValueError, SyntaxError):
                continue  # e.g. "[nan]" for the empty "Militär" category
            for job in jobs:
                if isinstance(job, str):
                    code_to_cat[job] = cat
    return code_to_cat, cat_names


# Further consolidation of the 9 main_branchen categories into 5 short-named
# super-categories, for a legend that's actually compact/legible rather than
# 9 long comma-separated names.
SUPER_CATEGORY_MAP = {
    "1": "A",
    "2": "A",
    "3": "A",
    "4": "B",
    "5": "C",
    "6": "C",
    "7": "D",
    "8": "E",
    "9": "E",
}
SUPER_CATEGORY_NAMES = {
    "A": "Trades & Production",
    "B": "STEM",
    "C": "Logistics & Trade",
    "D": "Business & Admin",
    "E": "Care, Culture & Education",
}


def load_code_to_super_category():
    """Map each 3-digit occupation code straight to one of 5 super-categories
    (consolidating the 9 main_branchen groups further, see SUPER_CATEGORY_MAP)."""
    code_to_broad, _ = load_code_to_broad_category()
    code_to_cat = {code: SUPER_CATEGORY_MAP[broad] for code, broad in code_to_broad.items()}
    return code_to_cat, dict(SUPER_CATEGORY_NAMES)
    return code_to_cat, cat_names


def load_real_world_male_pct_by_category(code_to_cat):
    """Real-world male % per BROAD occupation category (not per fine 3-digit
    code): with only ~8 source sentences per fine code (median), per-code
    points were dominated by sampling noise (many pinned at 0%/100%). Pooling
    to the 9 main_branchen categories gives 46-214 source rows -> ~300-1500
    pooled predictions per point, a much more reliable estimate."""
    totals = {}
    with open(
        "create_deval_synth/job_statistics/utilities/branchen_statistics.csv",
        newline="",
        encoding="utf-8",
    ) as f:
        for row in csv.DictReader(f, delimiter=";"):
            code = row["Code"]
            if code == "100" or code not in code_to_cat:  # romantic placeholder / unmapped
                continue
            try:
                m, f = int(row["Männer"]), int(row["Frauen"])
            except ValueError:
                continue
            cat = code_to_cat[code]
            tm, tf = totals.get(cat, (0, 0))
            totals[cat] = (tm + m, tf + f)
    return {cat: (m / (m + f) * 100) for cat, (m, f) in totals.items() if (m + f) > 0}


def figure_2_occupation_scatter(
    styles=(1, 2, 3, 4),
    suffix="",
    granularity="broad",
    figsize=(8.5, 8.5),
    marker_size=45,
    label_fontsize=8,
):
    loaders = {
        "fine": load_code_to_category,
        "broad": load_code_to_broad_category,
        "super": load_code_to_super_category,
    }
    code_to_cat, cat_names = loaders[granularity]()
    real_world_pct = load_real_world_male_pct_by_category(code_to_cat)

    present_cats = sorted(set(code_to_cat.values()) & set(cat_names))
    cmap = plt.get_cmap("turbo")
    cat_colors = {
        cat: cmap(i / max(1, len(present_cats) - 1)) for i, cat in enumerate(present_cats)
    }
    markers = {
        "google": "p",
        "google_llm": "P",
        "deepl": "s",
        "microsoft": "o",
        "systran": "d",
        "gpt-4o": "X",
    }

    fig, ax = plt.subplots(figsize=figsize)
    # Force the axes box itself to stay square regardless of how much width
    # subplots_adjust() below reserves for the legends -- otherwise the plot
    # area comes out taller than wide once the right margin is narrowed.
    ax.set_box_aspect(1)
    all_x, all_y = [], []

    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        # DIVERSE gold instances excluded -- out of scope for this pooled
        # binary occupation-bias view, handled separately in figs 7/7b/8/9.
        df = df[
            df["sentence_style"].isin(styles) & df["x_gender"].isin(["MASCULINE", "FEMININE"])
        ]
        df = df.copy()
        df["cat"] = df["x_group"].astype(str).map(code_to_cat)

        for cat, group in df.groupby("cat"):
            if cat not in real_world_pct:
                continue
            preds = []
            for lang in LANGUAGES:
                col = f"x_gender_{lang}"
                if col in group.columns:
                    preds.extend(group[col].tolist())
            n_m = preds.count("MASCULINE")
            n_f = preds.count("FEMININE")
            if n_m + n_f < 1:  # avoid division by zero; no other filtering
                continue
            pred_pct = n_m / (n_m + n_f) * 100

            x = real_world_pct[cat] - 50
            y = pred_pct - 50
            all_x.append(x)
            all_y.append(y)
            ax.scatter(
                x,
                y,
                marker=markers[model],
                color=cat_colors[cat],
                s=marker_size,
                edgecolors="grey",
                linewidths=0.4,
                alpha=0.85,
            )

    compact = granularity in ("broad", "super")
    fs = label_fontsize or (6 if compact else 7)

    # Correlation/trend line: linear fit of translated % on real-world %,
    # plus Pearson r. Slope < 1 means translation compresses the real-world
    # distribution toward 50/50; slope > 1 would mean it exaggerates it.
    # r alone doesn't say whether the correlation is meaningful -- always
    # report it together with n (how many points it's based on) and the
    # p-value (is it distinguishable from no correlation at all).
    slope, intercept = np.polyfit(all_x, all_y, 1)
    r, p = pearsonr(all_x, all_y)
    n = len(all_x)
    stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
    xs_line = np.array([-51, 51])
    ax.plot(xs_line, slope * xs_line + intercept, color="firebrick", lw=1.3, ls="-", zorder=1)
    # Label written directly on the line itself (near its left end, where
    # the data cloud is sparse), rotated to follow the line's slope --
    # square axes with equal x/y ranges mean the on-screen angle matches
    # atan(slope) directly.
    label_x = -46
    rotation_deg = np.degrees(np.arctan(slope))
    ax.text(
        label_x,
        slope * label_x + intercept + 1.5,
        f"r = {r:.2f} {stars}",
        color="firebrick",
        fontsize=fs,
        ha="left",
        va="bottom",
        fontweight="bold",
        rotation=rotation_deg,
        rotation_mode="anchor",
    )

    ax.set_xlim(-51, 51)
    ax.set_ylim(-51, 51)
    ax.set_xticks([-50, -25, 0, 25, 50])
    ax.set_xticklabels(["100", "75", "50/50", "75", "100"], fontsize=fs)
    ax.set_yticks([-50, -25, 0, 25, 50])
    ax.set_yticklabels(["100", "75", "50/50", "75", "100"], fontsize=fs)

    ax.axvline(0, c="k", lw=1.2 if compact else 1.5)
    ax.axhline(0, c="darkgreen", lw=1.2 if compact else 1.5)
    ax.axvline(25, c="grey", lw=0.4, ls="dashed")
    ax.axvline(-25, c="grey", lw=0.4, ls="dashed")
    ax.axhline(25, c="grey", lw=0.4, ls="dashed")
    ax.axhline(-25, c="grey", lw=0.4, ls="dashed")
    ax.fill_between([-51, 51], -5, 5, facecolor="darkgreen", alpha=0.1)
    ax.fill_betweenx([-51, 51], -5, 5, facecolor="grey", alpha=0.15)

    # Matches the original poster layout: "female"/"male" sit as a second
    # tier of labels BELOW the tick numbers (not above the plot), and the
    # axis title comes after that -- same idea mirrored vertically for the
    # y-axis (rotated, to the left of the tick numbers).
    ax.set_xlabel("Real-world gender distribution (%)", fontsize=fs + 1, labelpad=22)
    ax.set_ylabel("Gender distribution in translation (%)", fontsize=fs + 1, labelpad=22)
    qfs = fs - 0.5
    ax.text(-30, -60, "female", ha="center", va="top", fontsize=fs + 1, clip_on=False)
    ax.text(30, -60, "male", ha="center", va="top", fontsize=fs + 1, clip_on=False)
    ax.text(
        -65,
        -30,
        "female",
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=fs + 1,
        clip_on=False,
    )
    ax.text(
        -65,
        30,
        "male",
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=fs + 1,
        clip_on=False,
    )
    # Quadrant labels: y>0 means MORE MASCULINE predictions (pred_pct>50),
    # y<0 means more feminine -- so top row is "... with male transl.",
    # bottom row is "... with female transl." (earlier version had this
    # backwards on all four labels).
    # Pushed into the extreme corners (not the +-30/-45 "middle" positions)
    # so they stay clear of the data cluster and the trend line.
    # Moved inward from the extreme corners toward the middle of each
    # quadrant (was pinned at the very edge, overlapping the plot border).
    box_kwargs = dict(
        ha="center",
        fontsize=qfs,
        bbox=dict(facecolor="white", edgecolor="grey", boxstyle="round,pad=0.25", alpha=0.9),
    )
    ax.text(-27, 40, "stereotyp. female\nwith male transl.", va="top", **box_kwargs)
    ax.text(-27, -40, "stereotyp. female\nwith female transl.", va="bottom", **box_kwargs)
    ax.text(27, 40, "stereotyp. male\nwith male transl.", va="top", **box_kwargs)
    ax.text(27, -40, "stereotyp. male\nwith female transl.", va="bottom", **box_kwargs)

    cat_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=cat_colors[c],
            markersize=6,
            label=cat_names[c],
        )
        for c in present_cats
    ]
    model_handles = [
        plt.Line2D(
            [0],
            [0],
            marker=markers[m],
            color="w",
            markerfacecolor="k",
            markersize=6,
            label=MODEL_LABELS[m],
        )
        for m in MODELS
    ]
    # Reserve the right-hand fraction of the figure for the legends up front
    # (instead of relying on bbox_inches="tight" to auto-pad around
    # off-canvas legends, which left a large blank gap between the axes and
    # the legend box). Legends sit right at the reserved edge, and the model
    # legend is placed directly below the actual rendered bottom of the
    # category legend (measured after drawing) instead of a fixed guess --
    # avoids both overlap and a big empty gap between the two legends.
    legend_x = 0.66
    fig.subplots_adjust(right=legend_x - 0.02)
    # Top of the legend block lines up with the top of the axes (not the top
    # of the whole figure canvas), so the legend visually starts where the
    # diagram itself starts.
    ax_top = ax.get_position().y1 + 0.015

    leg1 = fig.legend(
        handles=cat_handles,
        title="Occupation category",
        loc="upper left",
        bbox_to_anchor=(legend_x, ax_top),
        fontsize=6.5,
        title_fontsize=7.5,
        labelspacing=0.4,
    )
    fig.add_artist(leg1)
    fig.canvas.draw()
    leg1_bottom_fig_y = fig.transFigure.inverted().transform((0, leg1.get_window_extent().y0))[1]
    fig.legend(
        handles=model_handles,
        title="MT system",
        loc="upper left",
        bbox_to_anchor=(legend_x, leg1_bottom_fig_y - 0.03),
        fontsize=6.5,
        title_fontsize=7.5,
    )

    path = os.path.join(OUTPUT_DIR, f"fig2_occupation_scatter{suffix}.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


def _binary_accuracy_by_style(model: str, style: int) -> float:
    """Accuracy (%) for one model, one sentence style, averaged over the 7
    languages -- masculine/feminine gold only (see load_binary_dataset)."""
    ds = load_binary_dataset(model, styles=(style,))
    error_df = ErrorAnalysis(ds, "x_gender").analyze(analyze_error_patterns=False)
    return error_df["accuracy"].astype(float).mean() * 100


# ---------------------------------------------------------------------------
# Figure 3: context-effect dumbbell chart (1.3 trans + 1.5 pronoun).
# Computed directly from processed_data (not outputs/summary/*.csv), which
# pooled DIVERSE gold instances in with masculine/feminine -- out of scope
# here, see load_binary_dataset.
# ---------------------------------------------------------------------------
def figure_3_context_effects():
    models_present = MODELS
    y = np.arange(len(models_present))

    fig, ax = plt.subplots(figsize=(6.5, 3.6))

    for i, model in enumerate(models_present):
        base = _binary_accuracy_by_style(model, 1)
        pron = _binary_accuracy_by_style(model, 2)
        trans = _binary_accuracy_by_style(model, 3)

        ax.plot([base, pron], [i + 0.15, i + 0.15], color="tab:blue", lw=2, zorder=1)
        ax.plot([base, trans], [i - 0.15, i - 0.15], color="tab:orange", lw=2, zorder=1)
        ax.scatter([base], [i + 0.15], color="grey", s=35, zorder=2)
        ax.scatter([base], [i - 0.15], color="grey", s=35, zorder=2)
        ax.scatter([pron], [i + 0.15], color="tab:blue", s=35, zorder=2)
        ax.scatter([trans], [i - 0.15], color="tab:orange", s=35, zorder=2)

        pron_delta = pron - base
        trans_delta = trans - base
        ax.text(
            max(base, pron) + 1.2,
            i + 0.15,
            f"+{pron_delta:.0f}%",
            va="center",
            fontsize=6.5,
            color="tab:blue",
        )
        ax.text(
            max(base, trans) + 1.2,
            i - 0.15,
            f"+{trans_delta:.0f}%",
            va="center",
            fontsize=6.5,
            color="tab:orange",
        )

    ax.set_yticks(y)
    ax.set_yticklabels([MODEL_LABELS[m] for m in models_present])
    ax.set_xlabel("Accuracy (%, averaged over 7 languages)")
    ax.set_xlim(40, 108)
    ax.grid(axis="x", alpha=0.3)
    ax.set_title("Effect of adding disambiguating context to the baseline sentence")

    legend_handles = [
        plt.Line2D([0], [0], color="grey", marker="o", label="Baseline"),
        plt.Line2D([0], [0], color="tab:blue", marker="o", label="+ pronoun"),
        plt.Line2D([0], [0], color="tab:orange", marker="o", label="+ trans-marking"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=7.5)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig3_context_effects.pdf")
    plt.savefig(path)
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 4: diverging bars for 1.4 (neutral names), pooled across 5 systems,
# with significance stars from analysis/significance.py. Used to be a 2-panel
# figure with heteronormativity (1.6) as panel B -- moved that to a table
# instead (table_heteronormativity_gap below): only 7 data points with small,
# partly non-significant differences, a bar chart implied more visual
# "weight" than the numbers support.
# ---------------------------------------------------------------------------
def figure_4_diverging_bias():
    fig, ax1 = plt.subplots(figsize=(4.5, 3.2))

    # Significance (test_direction_skew) is reported in the paper text
    # instead of on the chart itself -- keeps the bars uncluttered.
    masc_pct, fem_pct = [], []
    for lang in LANGUAGES:
        pooled_errors = []
        for model in ["google", "google_llm", "deepl", "microsoft", "systran"]:
            path = f"processed_data/romantic_names/romantic_name_{model}_processed.csv"
            if not os.path.exists(path):
                continue  # e.g. gpt-4o, still being translated in the background
            df = pd.read_csv(path, sep=";")
            sub = df[(df["sentence_style"] == 6) & (df["name_gender"] == "n")]
            col = f"x_gender_{lang}"
            if col not in sub.columns:
                continue
            pooled_errors.extend(
                (g, p)
                for g, p in zip(sub["x_gender"], sub[col])
                if pd.notna(p) and g != p and p in ("MASCULINE", "FEMININE")
            )
        result = test_direction_skew(pooled_errors)
        n = result["n"] or 1
        masc_pct.append(result.get("n_MASCULINE", 0) / n * 100)
        fem_pct.append(-result.get("n_FEMININE", 0) / n * 100)

    y = np.arange(len(LANGUAGES))
    ax1.barh(y, masc_pct, color=GENDER_COLORS["masculine"], label="-> masculine")
    ax1.barh(y, fem_pct, color=GENDER_COLORS["feminine"], label="-> feminine")
    for i in range(len(LANGUAGES)):
        if masc_pct[i] > 2:
            ax1.text(
                masc_pct[i] + 2,
                i,
                f"{masc_pct[i]:.0f}%",
                va="center",
                fontsize=6.5,
                color=GENDER_COLORS["masculine"],
            )
        if fem_pct[i] < -2:
            ax1.text(
                fem_pct[i] - 2,
                i,
                f"{-fem_pct[i]:.0f}%",
                va="center",
                ha="right",
                fontsize=6.5,
                color=GENDER_COLORS["feminine"],
            )
    ax1.set_yticks(y)
    ax1.set_yticklabels(LANGUAGES, fontsize=8)
    ax1.tick_params(axis="x", labelsize=7)
    ax1.axvline(0, color="k", lw=0.8)
    ax1.set_xlim(-105, 118)
    # Explicit caveat instead of just "5 systems": without this, a reader
    # can't tell whether the missing 6th system is a real exclusion or
    # incomplete data. GPT-4o's romantic-names translation is still running
    # in the background as of this figure's generation -- rerun once done.
    ax1.set_xlabel(
        "% of errors, pooled over 5 systems\n(GPT-4o excluded: translation pending)", fontsize=8
    )
    ax1.set_title("Neutral-name error direction", fontsize=9)
    # "lower right" used to sit directly on top of the es-row label (the
    # bottom-most bar, since es is first in LANGUAGES and barh plots it at
    # y=0) -- "upper right" sits next to he's small 18% masculine label,
    # which leaves it clear.
    ax1.legend(fontsize=7, loc="upper right")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig4_diverging_bias.pdf")
    plt.savefig(path)
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Table (not a figure): heteronormativity gap (1.6), was Figure 4 panel B.
# Writes both a LaTeX table (drop into the paper) and a CSV (for reference).
# ---------------------------------------------------------------------------
def table_heteronormativity_gap():
    # Paired design: every subject sentence is generated with BOTH a same-
    # gender and a different-gender partner (559/559 (sentence_id, x) groups
    # checked have both), so this is matched-pairs data, not two independent
    # samples -- McNemar's test (test_paired_gap) is the correct test here,
    # and is substantially more powerful than the chi-square-of-independence
    # test previously used (which discarded the pairing and treated the two
    # conditions as unrelated samples).
    rows = []
    for lang in LANGUAGES:
        correct_diff, correct_same = [], []
        for model in MODELS:
            path = f"processed_data/romantic_names/romantic_name_{model}_processed.csv"
            if not os.path.exists(path):
                continue  # e.g. gpt-4o, still being translated in the background
            df = pd.read_csv(path, sep=";")
            sub = df[df["sentence_style"] == 5]
            col = f"x_gender_{lang}"
            if col not in sub.columns:
                continue
            binary = sub[
                sub["x_gender"].isin(["MASCULINE", "FEMININE"])
                & sub["y_gender"].isin(["MASCULINE", "FEMININE"])
                & sub[col].notna()
            ].copy()
            binary["correct"] = binary["x_gender"] == binary[col]
            binary["pairing"] = np.where(binary["x_gender"] == binary["y_gender"], "same", "diff")
            piv = binary.pivot_table(
                index=["sentence_id", "x_nom_sg", "x_gender"], columns="pairing", values="correct", aggfunc="first"
            ).dropna()
            correct_diff.extend(piv["diff"].tolist())
            correct_same.extend(piv["same"].tolist())
        result = test_paired_gap(correct_diff, correct_same)
        hetero_acc = result["accuracy_a"] * 100
        same_acc = result["accuracy_b"] * 100
        gap = hetero_acc - same_acc
        p = result["p_value"]
        stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        rows.append(
            {
                "language": lang,
                "hetero_accuracy": hetero_acc,
                "same_gender_accuracy": same_acc,
                "gap": gap,
                "n": result["n"],
                "n_discordant": result["n_discordant"],
                "p_value": p,
                "significance": stars,
            }
        )

    df = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "table_heteronormativity_gap.csv")
    df.to_csv(csv_path, index=False)

    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"\textbf{Lang.} & \textbf{Hetero-coded (\%)} & \textbf{Same-gender (\%)} & \textbf{Gap} \\",
        r"\midrule",
    ]
    for r in rows:
        tex_lines.append(
            f"{r['language']} & {r['hetero_accuracy']:.1f} & {r['same_gender_accuracy']:.1f} "
            f"& +{r['gap']:.1f}{r['significance']} \\\\"
        )
    tex_lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Heteronormativity gap: accuracy on the occupation noun when the romantic "
        r"partner's gender matches (same-gender-coded) vs.\ differs from (hetero-coded) the "
        r"subject's gender, pooled over all 6 systems. Paired design (every subject sentence "
        r"is generated with both partner genders); significance via McNemar's test on the "
        r"matched pairs. "
        r"* $p<0.05$, ** $p<0.01$, *** $p<0.001$.}",
        r"\label{tab:heteronormativity_gap}",
        r"\end{table}",
    ]
    tex_path = os.path.join(OUTPUT_DIR, "table_heteronormativity_gap.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines) + "\n")

    print("Saved", csv_path)
    print("Saved", tex_path)
    print(df.to_string(index=False))


# ---------------------------------------------------------------------------
# Figure 5: stereotypicality vs. accuracy (replaces the odds-ratio forest
# plot). Uses the SAME predictor as the actual logistic regression (1.7):
# x_stereotypical, a per-INSTANCE value (does this specific instance's
# gender match the real-world majority for its occupation, 0-1) -- not a
# per-occupation-category aggregate. That distinction matters: averaging
# accuracy per category mixes pro- and anti-stereotypical instances of the
# same occupation and cancels the effect out (that was the bug in the first
# version of this figure -- pooled trend came out flat).
# ---------------------------------------------------------------------------
def _stereotypicality_lowess(model, styles, frac=0.3):
    """Per-instance (x_stereotypical, correct) pairs, pooled over all 7
    languages, smoothed with LOWESS -- avoids the binning artifact where a
    handful of occupations dominate a bin and shift its average (see the
    n_bins=10 version: only ~38 distinct occupations feed each bin, so 1-2
    unusual ones visibly move it, e.g. the bin-4 peak driven by 3 groups
    with 24-32 instances each).

    it=0 (no robustifying iterations): with it=1 (the default-ish choice),
    LOWESS's iterative reweighting treats the minority class (translation
    errors, since most predictions are correct) as "outliers" and downweights
    them more each iteration, inflating the curve toward ~100% at both edges
    where there's less data to stabilize the fit (verified: raw accuracy for
    GPT-4o at x>0.9 is 88.7%, but it=1 LOWESS reported 99.7% there). it=0
    avoids this and matches the raw sub-averages.
    """
    df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
    # DIVERSE gold excluded -- out of scope for this pooled binary view (see
    # load_binary_dataset); x_stereotypical is also only meaningfully defined
    # relative to a binary real-world gender split anyway.
    df = df[df["sentence_style"].isin(styles) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]

    xs, ys = [], []
    for lang in LANGUAGES:
        col = f"x_gender_{lang}"
        if col not in df.columns:
            continue
        gold, pred = df["x_gender"], df[col]
        is_correct = gold == pred
        xs.extend(df["x_stereotypical"].tolist())
        ys.extend((is_correct.astype(float) * 100).tolist())

    smoothed = lowess(ys, xs, frac=frac, it=0, return_sorted=True)
    return smoothed[:, 0], smoothed[:, 1]


def figure_5_stereotypicality_scatter(styles=(1, 2, 3, 4)):
    model_colors = {
        "google": "tab:blue",
        "google_llm": "tab:cyan",
        "deepl": "tab:green",
        "microsoft": "tab:purple",
        "systran": "tab:orange",
        "gpt-4o": "tab:red",
    }

    fig, ax = plt.subplots(figsize=(3.6, 3.0))

    for model in MODELS:
        x_smooth, y_smooth = _stereotypicality_lowess(model, styles)
        lw = 2.0 if model == "gpt-4o" else 1.1
        alpha = 1.0 if model == "gpt-4o" else 0.7
        # x_smooth is a 0-1 proportion (num_g/(num_m+num_f)); shown as 0-100 (%)
        ax.plot(
            x_smooth * 100,
            y_smooth,
            color=model_colors[model],
            lw=lw,
            alpha=alpha,
            label=MODEL_LABELS[model],
        )

    ax.axvline(50, color="grey", lw=0.8, ls=":")
    ax.set_xlim(0, 100)
    # Mirrored 100 -> 0 -> 100 scale, like figure 2's female/male axis: the
    # displayed number is the distance from the center (parity, x_stereotypical
    # = 0.5) doubled to a 0-100 range, so both edges (pure counter-stereotype
    # and pure stereotype) read "100" and the middle reads "0". The underlying
    # data position is untouched (still raw x_stereotypical*100) -- only the
    # tick labels change.
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["100", "50", "0", "50", "100"])
    ax.set_xlabel("Instance stereotypicality (%)", fontsize=7.5, labelpad=16)
    ax.set_ylabel("Translation accuracy (%)", fontsize=7.5)
    ax.tick_params(labelsize=7)
    ymin, ymax = ax.get_ylim()
    # Same visual language as figure 2's "female"/"male" sub-labels below the
    # tick numbers, here "counterstereotype"/"stereotype" instead.
    ypos = ymin - 0.10 * (ymax - ymin)
    ax.text(20, ypos, "counterstereotype", ha="center", va="top", fontsize=7, clip_on=False)
    ax.text(80, ypos, "stereotype", ha="center", va="top", fontsize=7, clip_on=False)
    ax.set_title("Does stereotype-congruence predict accuracy?", fontsize=8.5)
    ax.legend(fontsize=6, loc="best")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig5_stereotypicality_scatter.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 2+5 combined: the compact broad-category occupation scatter (left)
# next to the stereotype-congruence-vs-accuracy line chart (right), as one
# figure -- both are about the same underlying question (does stereotyping
# shape/predict translation behavior), just from two angles.
# ---------------------------------------------------------------------------
def figure_2_5_combined(scatter_styles=(1, 2, 3, 4), line_styles=(1, 2, 3, 4)):
    code_to_cat, cat_names = load_code_to_broad_category()
    real_world_pct = load_real_world_male_pct_by_category(code_to_cat)
    present_cats = sorted(set(code_to_cat.values()) & set(cat_names))
    cmap = plt.get_cmap("turbo")
    cat_colors = {
        cat: cmap(i / max(1, len(present_cats) - 1)) for i, cat in enumerate(present_cats)
    }
    markers = {
        "google": "p",
        "google_llm": "P",
        "deepl": "s",
        "microsoft": "o",
        "systran": "d",
        "gpt-4o": "X",
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.0))

    # --- Left: occupation scatter (same as figure_2_occupation_scatter, granularity="broad") ---
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        df = df[df["sentence_style"].isin(scatter_styles)].copy()
        df["cat"] = df["x_group"].astype(str).map(code_to_cat)
        for cat, group in df.groupby("cat"):
            if cat not in real_world_pct:
                continue
            preds = []
            for lang in LANGUAGES:
                col = f"x_gender_{lang}"
                if col in group.columns:
                    preds.extend(group[col].tolist())
            n_m, n_f = preds.count("MASCULINE"), preds.count("FEMININE")
            if n_m + n_f < 1:
                continue
            pred_pct = n_m / (n_m + n_f) * 100
            ax1.scatter(
                real_world_pct[cat] - 50,
                pred_pct - 50,
                marker=markers[model],
                color=cat_colors[cat],
                s=30,
                edgecolors="grey",
                linewidths=0.4,
                alpha=0.85,
            )

    ax1.set_xlim(-51, 51)
    ax1.set_ylim(-51, 51)
    ax1.set_xticks([-50, -25, 0, 25, 50])
    ax1.set_xticklabels(["100", "75", "50/50", "75", "100"], fontsize=6)
    ax1.set_yticks([-50, -25, 0, 25, 50])
    ax1.set_yticklabels(["100", "75", "50/50", "75", "100"], fontsize=6)
    ax1.axvline(0, c="k", lw=1.2)
    ax1.axhline(0, c="darkgreen", lw=1.2)
    ax1.axvline(25, c="grey", lw=0.4, ls="dashed")
    ax1.axvline(-25, c="grey", lw=0.4, ls="dashed")
    ax1.axhline(25, c="grey", lw=0.4, ls="dashed")
    ax1.axhline(-25, c="grey", lw=0.4, ls="dashed")
    ax1.fill_between([-51, 51], -5, 5, facecolor="darkgreen", alpha=0.1)
    ax1.fill_betweenx([-51, 51], -5, 5, facecolor="grey", alpha=0.15)
    ax1.set_xlabel("Real-world gender distribution (%)", fontsize=7)
    ax1.set_ylabel("Gender distribution in translation (%)", fontsize=7)
    ax1.text(-30, 40, "female", ha="center", fontsize=7)
    ax1.text(30, 40, "male", ha="center", fontsize=7)
    ax1.text(
        -45,
        -30,
        "stereotyp. female\nwith male transl.",
        ha="center",
        fontsize=5.5,
        bbox=dict(facecolor="white", edgecolor="grey", boxstyle="round,pad=0.3"),
    )
    ax1.text(
        -45,
        30,
        "stereotyp. female\nwith female transl.",
        ha="center",
        fontsize=5.5,
        bbox=dict(facecolor="white", edgecolor="grey", boxstyle="round,pad=0.3"),
    )
    ax1.text(
        45,
        -30,
        "stereotyp. male\nwith male transl.",
        ha="center",
        fontsize=5.5,
        bbox=dict(facecolor="white", edgecolor="grey", boxstyle="round,pad=0.3"),
    )
    ax1.text(
        45,
        30,
        "stereotyp. male\nwith female transl.",
        ha="center",
        fontsize=5.5,
        bbox=dict(facecolor="white", edgecolor="grey", boxstyle="round,pad=0.3"),
    )
    ax1.set_title("A. Direction of bias", fontsize=9)

    # --- Right: stereotype-congruence vs. accuracy (same as figure_5) ---
    model_colors = {
        "google": "tab:blue",
        "google_llm": "tab:cyan",
        "deepl": "tab:green",
        "microsoft": "tab:purple",
        "systran": "tab:orange",
        "gpt-4o": "tab:red",
    }
    for model in MODELS:
        x_smooth, y_smooth = _stereotypicality_lowess(model, line_styles)
        lw = 2.2 if model == "gpt-4o" else 1.2
        alpha = 1.0 if model == "gpt-4o" else 0.7
        ax2.plot(
            x_smooth,
            y_smooth,
            color=model_colors[model],
            lw=lw,
            alpha=alpha,
            label=MODEL_LABELS[model],
        )
    ax2.axvline(0.5, color="grey", lw=0.8, ls=":")
    ax2.set_xlabel("Instance stereotypicality\n(0 = counter-stereotype, 1 = congruent)", fontsize=7)
    ax2.set_ylabel("Translation accuracy (%)", fontsize=7)
    ax2.tick_params(labelsize=6)
    ax2.legend(fontsize=6, loc="lower right")
    ax2.grid(alpha=0.3)
    ax2.set_title("B. Does stereotype-congruence predict accuracy?", fontsize=9)

    cat_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=cat_colors[c],
            markersize=6,
            label=cat_names[c],
        )
        for c in present_cats
    ]
    model_handles = [
        plt.Line2D(
            [0],
            [0],
            marker=markers[m],
            color="w",
            markerfacecolor="k",
            markersize=6,
            label=MODEL_LABELS[m],
        )
        for m in MODELS
    ]
    fig.legend(
        handles=cat_handles,
        title="Occupation category (panel A color)",
        loc="upper left",
        bbox_to_anchor=(0.5, -0.02),
        fontsize=6,
        title_fontsize=7,
        ncol=3,
        labelspacing=0.4,
    )
    fig.legend(
        handles=model_handles,
        title="MT system (panel A marker)",
        loc="upper left",
        bbox_to_anchor=(0.02, -0.02),
        fontsize=6,
        title_fontsize=7,
        ncol=1,
        labelspacing=0.4,
    )

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig2_5_combined.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Table (not a figure): logistic regression / odds ratios (1.7), was Figure 6.
# GPT-4o only -- that's also what the reported finding (1.21-1.43, Hebrew
# reversal) is actually about. A table instead of a forest plot: with only 7
# rows and CIs that don't overlap much, a table reads faster than a chart and
# keeps the same "numbers over bar/point charts for small-n results" pattern
# already used for table_heteronormativity_gap.
#
# Computed directly (not from outputs/{model}_logistic_regression.csv), which
# pooled DIVERSE gold instances in with masculine/feminine -- out of scope
# here, see load_binary_dataset. DIVERSE rows would never actually match a
# predicted value (pred can never literally be "DIVERSE"), so they always
# counted as incorrect regardless of x_stereotypical -- quietly pulling the
# regression toward "high stereotypicality -> incorrect" for reasons that had
# nothing to do with stereotypicality.
# ---------------------------------------------------------------------------
def table_logistic_regression(model="gpt-4o", compare_model="google"):
    # compare_model added to show whether GPT-4o's flatter stereotype-
    # dependence (smaller odds ratios, see \S\ref{sec:results}.7) is a
    # GPT-4o-specific property or common to all systems: Google's odds
    # ratios are 1.4-2x larger than GPT-4o's in every non-Hebrew language,
    # and Hebrew's reversal (OR<1) turns out to be GPT-4o-specific too --
    # Google shows no significant relationship in Hebrew at all (p=0.61).
    def _compute(m):
        ds = load_binary_dataset(m)
        lr_df = LogisticRegressionAnalysis(ds, "x_gender").analyze(predictor_col="x_stereotypical")
        out = {}
        for lang in LANGUAGES:
            row = lr_df[lr_df["language"] == lang]
            if row.empty:
                continue
            row = row.iloc[0]
            out[lang] = {
                "odds_ratio": row["odds_ratio"],
                "ci_lower": row["ci_lower"],
                "ci_upper": row["ci_upper"],
                "p_value": row["p_value"],
                "n": int(row["n_observations"]),
            }
        return out

    def _stars(p):
        return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""

    main_vals = _compute(model)
    cmp_vals = _compute(compare_model)

    rows = []
    for lang in LANGUAGES:
        if lang not in main_vals or lang not in cmp_vals:
            continue
        m, c = main_vals[lang], cmp_vals[lang]
        rows.append(
            {
                "language": lang,
                "odds_ratio": m["odds_ratio"],
                "ci_lower": m["ci_lower"],
                "ci_upper": m["ci_upper"],
                "p_value": m["p_value"],
                "n": m["n"],
                "significance": _stars(m["p_value"]),
                f"odds_ratio_{compare_model}": c["odds_ratio"],
                f"p_value_{compare_model}": c["p_value"],
                f"significance_{compare_model}": _stars(c["p_value"]),
            }
        )

    out_df = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "table_logistic_regression.csv")
    out_df.to_csv(csv_path, index=False)

    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\begin{tabular}{lcc}",
        r"\toprule",
        rf"\textbf{{Lang.}} & \textbf{{OR ({MODEL_LABELS[model]})}} & \textbf{{OR ({MODEL_LABELS[compare_model]})}} \\",
        r"\midrule",
    ]
    for r in rows:
        tex_lines.append(
            f"{r['language']} & {r['odds_ratio']:.2f}{r['significance']} & "
            f"{r[f'odds_ratio_{compare_model}']:.2f}{r[f'significance_{compare_model}']} \\\\"
        )
    tex_lines += [
        r"\bottomrule",
        r"\end{tabular}",
        rf"\caption{{Logistic regression: odds ratio for stereotype-congruence predicting a "
        rf"correct translation, per language, {MODEL_LABELS[model]} vs.\ {MODEL_LABELS[compare_model]} "
        r"(95\% CI and exact $p$ for the full "
        rf"{MODEL_LABELS[model]} model in \texttt{{table\_logistic\_regression.csv}}). "
        r"OR $>$1 means more accurate when stereotype-congruent. "
        rf"{MODEL_LABELS[compare_model]}'s odds ratios are descriptively larger than "
        rf"{MODEL_LABELS[model]}'s in every non-Hebrew language (not a formally tested "
        r"interaction -- two separately-fit sets of per-language models); Hebrew's reversal (OR$<$1) is "
        rf"{MODEL_LABELS[model]}-specific -- {MODEL_LABELS[compare_model]} shows no significant "
        r"relationship there at all. "
        r"* $p<0.05$, ** $p<0.01$, *** $p<0.001$.}",
        r"\label{tab:logistic_regression}",
        r"\end{table}",
    ]
    tex_path = os.path.join(OUTPUT_DIR, "table_logistic_regression.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines) + "\n")

    print("Saved", csv_path)
    print("Saved", tex_path)
    print(out_df.to_string(index=False))


# ---------------------------------------------------------------------------
# Shared helper for both human-eval tables below: human-eval "match"
# judgments vs. the pipeline's own gold/predicted gender, joined via
# human_eval/outputs/metadata/*_metadata.csv (Translator + Index ->
# Source_File_Line, a 1-indexed *file* line number including the header, so
# the row in processed_data is at Source_File_Line - 2). Validates the
# automatic evaluation pipeline itself: does a human agree the MT output's
# gender matches what the pipeline extracted, independent of whether that
# matches the German gold?
#
# Many sentences were judged by more than one participant (up to 9, across
# the 3 collection rounds) while others were only judged once -- comparing
# every individual judgment would silently over-weight the heavily-annotated
# sentences. Instead take a majority vote (yes/no, "idk" excluded unless
# that's the only answer) per unique (language, translator, index) sentence
# first, then compare that one verdict per sentence against the pipeline.
# Exact ties (possible with an even number of judgments) are dropped.
# ---------------------------------------------------------------------------
def _majority_vote_per_sentence(question, valid_values=("yes", "no")):
    """Majority vote per unique (language, translator, index) sentence for
    the given Question ("gender", "makesense", ...). Ties dropped."""
    translator_to_model = {
        "Deepl": "deepl", "Google": "google", "Gpt-4o": "gpt-4o",
        "Microsoft": "microsoft", "Systran": "systran",
    }
    # ar excluded: only one annotator (human_eval/results-20260204/ar-*.csv)
    # took part, so its "majority vote" is really just one person's opinion,
    # not a genuine consensus -- not reliable enough to report.
    lang_file_to_code = {"sp": "es", "fr": "fr", "it": "it", "ru": "ru", "uk": "uk", "he": "he"}

    judgments = []
    for path in glob.glob("human_eval/results-*/*.csv"):
        file_lang = os.path.basename(path).split("-")[0]
        if file_lang not in lang_file_to_code:
            continue
        lang = lang_file_to_code[file_lang]
        df = pd.read_csv(path)
        for _, r in df[df["Question"] == question].iterrows():
            if r["translator"] not in translator_to_model:
                continue
            judgments.append(
                {"lang": lang, "translator": r["translator"], "index": r["index"], "value": r["Value"]}
            )
    jdf = pd.DataFrame(judgments)

    votes = {}
    for (lang, translator, idx), g in jdf.groupby(["lang", "translator", "index"]):
        counts = g["value"].value_counts()
        counts = counts[counts.index.isin(valid_values)]
        if counts.empty:
            continue  # every judgment was "idk"/"notsure"
        if len(counts) > 1 and counts.iloc[0] == counts.iloc[1]:
            continue  # exact tie, drop
        votes[(lang, translator, idx)] = counts.idxmax()
    return votes


# Human-eval Question 2 ("gender": what gender is the job description in the
# sentence?) values -> the pipeline's gender labels.
_HUMAN_GENDER_MAP = {"m": "MASCULINE", "f": "FEMININE", "n": "NEUTER"}


def _human_eval_votes_vs_pipeline():
    """Compares human-perceived gender (Question 2, "gender") against the
    pipeline's own prediction, both scored against the same German gold --
    NOT Question 1 ("match", which validates word alignment/extraction, a
    different thing from gender correctness)."""
    translator_to_model = {
        "Deepl": "deepl",
        "Google": "google",
        "Gpt-4o": "gpt-4o",
        "Microsoft": "microsoft",
        "Systran": "systran",
    }

    proc_cache: dict = {}

    def get_proc(model):
        if model not in proc_cache:
            proc_cache[model] = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        return proc_cache[model]

    meta_cache: dict = {}

    def get_meta(lang):
        if lang not in meta_cache:
            meta_cache[lang] = pd.read_csv(
                f"human_eval/outputs/metadata/{lang}_Multi_hev_metadata.csv", sep=";"
            )
        return meta_cache[lang]

    gender_votes = _majority_vote_per_sentence("gender", valid_values=("m", "f", "n"))

    def gold_pred_for(lang, translator, idx):
        meta = get_meta(lang)
        model = translator_to_model[translator]
        meta_row = meta[(meta["Translator"] == translator) & (meta["Index"] == idx)]
        if meta_row.empty:
            return None, None
        proc = get_proc(model)
        pos = int(meta_row.iloc[0]["Source_File_Line"]) - 2
        if pos < 0 or pos >= len(proc):
            return None, None
        prow = proc.iloc[pos]
        return prow["x_gender"], prow.get(f"x_gender_{lang}")

    rows = []
    for (lang, translator, idx), human_val in gender_votes.items():
        gold, pred = gold_pred_for(lang, translator, idx)
        if gold is None:
            continue
        # Pipeline UNKNOWN is the direct equivalent of a human "idk" -- we
        # already exclude "idk" from the human votes (valid_values above), so
        # for a fair comparison UNKNOWN pipeline predictions are excluded
        # here too, instead of automatically counting as a pipeline miss.
        if pred == "UNKNOWN":
            continue
        human_gender = _HUMAN_GENDER_MAP[human_val]
        human_correct = (human_gender == gold) or (gold == "DIVERSE" and human_gender == "NEUTER")
        pipeline_correct = (pred == gold) or (gold == "DIVERSE" and pred == "NEUTER")
        rows.append(
            {
                "lang": lang,
                "translator": translator,
                "index": idx,
                "human_gender": human_gender,
                "pipeline_gender": pred,
                "gold": gold,
                "human_says_ok": human_correct,
                "pipeline_correct": pipeline_correct,
                "model": translator_to_model[translator],
            }
        )
    return pd.DataFrame(rows)


def print_alignment_match_rate():
    """Question 1 ("match": does the extracted expression refer to the same
    job title as the sentence's subject?) validates the ALIGNMENT step of
    the pipeline -- a distinct claim from the gender-accuracy tables above,
    which validate the morphological-analysis step. Not filtered by
    "makesense", since alignment success doesn't depend on translation
    quality the way gender-extraction correctness does."""
    match_votes = _majority_vote_per_sentence("match", valid_values=("yes", "no"))
    n = len(match_votes)
    yes_n = sum(1 for v in match_votes.values() if v == "yes")
    print(f"Alignment match rate (all languages): {yes_n}/{n} = {yes_n / n * 100:.1f}%")

    from collections import defaultdict

    by_lang = defaultdict(list)
    for (lang, translator, idx), v in match_votes.items():
        by_lang[lang].append(v)
    rows = [{"language": "all", "n": n, "yes": yes_n, "match_rate_pct": round(yes_n / n * 100, 1)}]
    for lang in LANGUAGES:
        vals = by_lang.get(lang, [])
        if not vals:
            continue
        yn = sum(1 for v in vals if v == "yes")
        print(f"  {lang}: {yn}/{len(vals)} = {yn / len(vals) * 100:.1f}%")
        rows.append(
            {"language": lang, "n": len(vals), "yes": yn, "match_rate_pct": round(yn / len(vals) * 100, 1)}
        )
    csv_path = os.path.join(OUTPUT_DIR, "human_eval_alignment_match_rate.csv")
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print("Saved", csv_path)


def print_human_eval_reliability_baseline():
    """Not a table for the paper -- a sanity check printed to the console,
    on Question 2 ("gender"): is the pipeline's accuracy gap vs. human
    annotators (table_human_eval_by_model/_agreement) actually a pipeline
    weakness, or is human annotation on this task just inherently noisy?
    Computes (1) pairwise inter-annotator agreement (do two annotators pick
    the same gender label for the same sentence?), and (2) a leave-one-out
    check: does a single held-out annotator's individual verdict match the
    MAJORITY of the *other* annotators on that sentence, at the same rate
    the pipeline matches the full human majority? This is the fair
    apples-to-apples comparison for "is the pipeline as good as a human
    annotator" -- both are being compared to a majority-of-the-rest, not to
    each other directly."""
    # ar excluded: only one annotator took part (see _majority_vote_per_sentence).
    lang_file_to_code = {"sp": "es", "fr": "fr", "it": "it", "ru": "ru", "uk": "uk", "he": "he"}
    translator_to_model = {
        "Deepl": "deepl", "Google": "google", "Gpt-4o": "gpt-4o",
        "Microsoft": "microsoft", "Systran": "systran",
    }

    judgments = []
    for path in glob.glob("human_eval/results-*/*.csv"):
        file_lang = os.path.basename(path).split("-")[0]
        if file_lang not in lang_file_to_code:
            continue
        lang = lang_file_to_code[file_lang]
        df = pd.read_csv(path)
        for _, r in df[df["Question"] == "gender"].iterrows():
            if r["translator"] not in translator_to_model:
                continue
            if r["Value"] not in _HUMAN_GENDER_MAP:
                continue  # excludes "idk"
            judgments.append(
                {"lang": lang, "translator": r["translator"], "index": r["index"], "value": r["Value"]}
            )
    jdf = pd.DataFrame(judgments)

    import itertools
    from collections import Counter

    multi_judgment_sentences = 0
    unanimous = 0
    agree_pairs = 0
    total_pairs = 0
    loo_total = 0
    loo_agree = 0

    for (lang, translator, idx), g in jdf.groupby(["lang", "translator", "index"]):
        vals = list(g["value"])
        if len(vals) > 1:
            multi_judgment_sentences += 1
            if len(set(vals)) == 1:
                unanimous += 1
            for a, b in itertools.combinations(vals, 2):
                total_pairs += 1
                if a == b:
                    agree_pairs += 1
        if len(vals) >= 3:  # need >=2 others to form a majority
            for i in range(len(vals)):
                others = vals[:i] + vals[i + 1:]
                counts = Counter(others)
                top = counts.most_common()
                if len(top) > 1 and top[0][1] == top[1][1]:
                    continue  # tie among the others
                loo_total += 1
                if vals[i] == top[0][0]:
                    loo_agree += 1

    print(f"n sentences with >1 judgment: {multi_judgment_sentences}")
    print(f"  unanimous among humans: {unanimous} ({unanimous / multi_judgment_sentences * 100:.1f}%)")
    print(f"  pairwise human-human agreement: {agree_pairs / total_pairs * 100:.1f}% (n_pairs={total_pairs})")
    print(
        f"  leave-one-out: single annotator vs. majority of the rest: "
        f"{loo_agree / loo_total * 100:.1f}% (n={loo_total})"
    )

    out_df = pd.DataFrame(
        [
            {
                "n_multi_judgment_sentences": multi_judgment_sentences,
                "n_unanimous": unanimous,
                "unanimous_pct": round(unanimous / multi_judgment_sentences * 100, 1),
                "n_pairs": total_pairs,
                "pairwise_agreement_pct": round(agree_pairs / total_pairs * 100, 1),
                "n_loo": loo_total,
                "loo_agreement_pct": round(loo_agree / loo_total * 100, 1),
            }
        ]
    )
    csv_path = os.path.join(OUTPUT_DIR, "human_eval_reliability_baseline.csv")
    out_df.to_csv(csv_path, index=False)
    print("Saved", csv_path)


def table_human_eval_agreement():
    """Per-language: human accuracy (majority-vote Question-2 gender judgment
    vs. gold) next to the pipeline's own accuracy on the identical sentences.
    Mirrors table_human_eval_by_model, grouped by language instead of system."""
    vdf = _human_eval_votes_vs_pipeline()
    rows = []
    for lang in LANGUAGES:
        g = vdf[vdf["lang"] == lang]
        if g.empty:
            continue
        n = len(g)
        human_acc = g["human_says_ok"].mean() * 100
        pipeline_acc = g["pipeline_correct"].mean() * 100
        rows.append(
            {"language": lang, "n": n, "human_accuracy": human_acc, "pipeline_accuracy": pipeline_acc, "gap": human_acc - pipeline_acc}
        )
    n_all = len(vdf)
    human_acc_all = vdf["human_says_ok"].mean() * 100
    pipeline_acc_all = vdf["pipeline_correct"].mean() * 100
    rows.append(
        {
            "language": "all",
            "n": n_all,
            "human_accuracy": human_acc_all,
            "pipeline_accuracy": pipeline_acc_all,
            "gap": human_acc_all - pipeline_acc_all,
        }
    )

    out_df = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "table_human_eval_agreement.csv")
    out_df.to_csv(csv_path, index=False)

    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{Lang.} & \textbf{$n$} & \textbf{Human} & \textbf{Pipeline} & \textbf{Gap} \\",
        r"\midrule",
    ]
    for r in rows:
        lang_label = r"\textit{all}" if r["language"] == "all" else r["language"]
        tex_lines.append(
            f"{lang_label} & {r['n']} & {r['human_accuracy']:.1f}\\% & "
            f"{r['pipeline_accuracy']:.1f}\\% & +{r['gap']:.1f}pp \\\\"
        )
    tex_lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Per-language accuracy on the human-eval sample: human majority-vote gender "
        r"judgment (Question 2) vs.\ the pipeline's own gold-vs-predicted accuracy, on the identical "
        r"sentences. Both are scored against the same German gold, not against each other. ar "
        r"excluded: only one annotator took part, so its result is not a genuine majority vote.}",
        r"\label{tab:human_eval_agreement}",
        r"\end{table}",
    ]
    tex_path = os.path.join(OUTPUT_DIR, "table_human_eval_agreement.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines) + "\n")

    print("Saved", csv_path)
    print("Saved", tex_path)
    print(out_df.to_string(index=False))


# ---------------------------------------------------------------------------
# Table (not a figure): per-system accuracy as perceived by human annotators
# (majority-vote `match' rate) vs. the pipeline's own accuracy, on the exact
# same sample of sentences. Reveals that the pipeline systematically
# under-credits every system relative to human judgment -- not just a random
# scatter of disagreements, but a consistent direction and a gap that shrinks
# for the strongest system (GPT-4o) and is largest for the weakest one we
# have human data for (SYSTRAN). Worth flagging prominently in Limitations:
# the *absolute* accuracy numbers in \S\ref{sec:results}.1 likely understate
# true system quality, though the relative *ranking* of systems is preserved.
# ---------------------------------------------------------------------------
def table_human_eval_by_model():
    vdf = _human_eval_votes_vs_pipeline()
    rows = []
    for model in MODELS:
        g = vdf[vdf["model"] == model]
        if g.empty:
            continue
        n = len(g)
        human_acc = g["human_says_ok"].mean() * 100
        pipeline_acc = g["pipeline_correct"].mean() * 100
        rows.append(
            {
                "model": MODEL_LABELS[model],
                "n": n,
                "human_accuracy": human_acc,
                "pipeline_accuracy": pipeline_acc,
                "gap": human_acc - pipeline_acc,
            }
        )

    out_df = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "table_human_eval_by_model.csv")
    out_df.to_csv(csv_path, index=False)

    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{System} & \textbf{$n$} & \textbf{Human} & \textbf{Pipeline} & \textbf{Gap} \\",
        r"\midrule",
    ]
    for r in rows:
        tex_lines.append(
            f"{r['model']} & {r['n']} & {r['human_accuracy']:.1f}\\% & "
            f"{r['pipeline_accuracy']:.1f}\\% & +{r['gap']:.1f}pp \\\\"
        )
    tex_lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Per-system accuracy on the human-eval sample, restricted to sentences where the "
        r"pipeline produced a definite prediction rather than UNKNOWN -- the pipeline's equivalent of "
        r"a human `idk', which is excluded from the human vote on the same grounds: human "
        r"majority-vote gender judgment (Question 2) vs.\ the pipeline's own gold-vs-predicted "
        r"accuracy, on the identical sentences, both scored against the same German gold. ar "
        r"excluded (only one annotator). GPT-4o comes closest to matching human accuracy.}",
        r"\label{tab:human_eval_by_model}",
        r"\end{table}",
    ]
    tex_path = os.path.join(OUTPUT_DIR, "table_human_eval_by_model.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines) + "\n")

    print("Saved", csv_path)
    print("Saved", tex_path)
    print(out_df.to_string(index=False))


def print_winomt_style_agreement():
    """WinoMT's (Stanovsky et al., 2019) own human-eval validation compares
    the human annotation of an entity's gender directly to the automatic
    method's OUTPUT (not to gold) and reports the agreement rate -- a
    different (and simpler) statistic than the gold-vs-both accuracy
    comparison in table_human_eval_by_model. Prints the same statistic here,
    for a direct, like-for-like comparison to their reported numbers
    (85%+ per system/language, 87% average; human inter-annotator
    agreement 90%)."""
    vdf = _human_eval_votes_vs_pipeline()
    overall = (vdf["human_gender"] == vdf["pipeline_gender"]).mean() * 100
    print(f"Overall direct agreement (human annotation vs. pipeline output): {overall:.1f}%")

    rows = [{"level": "overall", "key": "all", "n": len(vdf), "agreement_pct": round(overall, 1)}]

    print("Per system:")
    for model in MODELS:
        g = vdf[vdf["model"] == model]
        if g.empty:
            continue
        a = (g["human_gender"] == g["pipeline_gender"]).mean() * 100
        print(f"  {MODEL_LABELS[model]}: {a:.1f}% (n={len(g)})")
        rows.append({"level": "system", "key": model, "n": len(g), "agreement_pct": round(a, 1)})

    print("Per language:")
    for lang in LANGUAGES:
        g = vdf[vdf["lang"] == lang]
        if g.empty:
            continue
        a = (g["human_gender"] == g["pipeline_gender"]).mean() * 100
        print(f"  {lang}: {a:.1f}% (n={len(g)})")
        rows.append({"level": "language", "key": lang, "n": len(g), "agreement_pct": round(a, 1)})

    cells = []
    for model in MODELS:
        for lang in LANGUAGES:
            g = vdf[(vdf["model"] == model) & (vdf["lang"] == lang)]
            if g.empty:
                continue
            a = (g["human_gender"] == g["pipeline_gender"]).mean() * 100
            cells.append(a)
            rows.append(
                {"level": "system_language", "key": f"{model}/{lang}", "n": len(g), "agreement_pct": round(a, 1)}
            )
    print(f"Per system-language cell range: {min(cells):.1f}%-{max(cells):.1f}%")

    csv_path = os.path.join(OUTPUT_DIR, "human_eval_winomt_style_agreement.csv")
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print("Saved", csv_path)


# ---------------------------------------------------------------------------
# Figure 7b: "Waehlerwanderung"-style alluvial/flow diagram -- gold gender
# (left) flowing to predicted outcome (right, including UNKNOWN and the tiny
# NEUTER remainder folded into it), one small-multiple panel per system.
# Captures the same statement as figure_7_error_rate_by_gender (how often is
# each gold gender mistranslated) but makes the UNKNOWN share visible as its
# own destination instead of hiding it inside an aggregate error rate, and
# shows the masculine-default direction as ribbon thickness at a glance.
# ---------------------------------------------------------------------------
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle


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


def figure_7_gender_flow_sankey():
    node_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    gold_order = ("MASCULINE", "FEMININE")
    pred_order = ("MASCULINE", "FEMININE", "UNKNOWN")

    fig, axes = plt.subplots(2, 3, figsize=(9, 6.0))
    for ax, model in zip(axes.flat, MODELS):
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        flows = {}
        # Per-language error rate (1 - recall) for each gold gender, so the
        # pooled Sankey ribbons can be annotated with mean +/- std across the
        # 7 languages -- otherwise the diagram can't distinguish "consistent
        # bias in every language" from "one extreme language driving the
        # pooled total", which the old bar chart's error bars showed.
        fem_err_by_lang, masc_err_by_lang = [], []
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            s = sub[sub[col].notna()]
            for gold, pred in zip(s["x_gender"], s[col]):
                # NEUTER folded into UNKNOWN: both mean "no definite binary
                # answer", and NEUTER is <1% of predictions here (unlike the
                # DIVERSE-gold case, where NEUTER is the meaningful proxy).
                pred_bucket = pred if pred in ("MASCULINE", "FEMININE") else "UNKNOWN"
                flows[(gold, pred_bucket)] = flows.get((gold, pred_bucket), 0) + 1
            fem_lang = s[s["x_gender"] == "FEMININE"]
            masc_lang = s[s["x_gender"] == "MASCULINE"]
            fem_err_by_lang.append((fem_lang[col] != "FEMININE").mean() * 100)
            masc_err_by_lang.append((masc_lang[col] != "MASCULINE").mean() * 100)
        _draw_sankey_panel(ax, flows, gold_order, pred_order, node_colors)
        ax.set_title(MODEL_LABELS[model], fontsize=10)
        ax.text(
            0.5,
            -0.1,
            f"error rate: fem {np.mean(fem_err_by_lang):.0f}$\\pm${np.std(fem_err_by_lang):.0f}pp, "
            f"masc {np.mean(masc_err_by_lang):.0f}$\\pm${np.std(masc_err_by_lang):.0f}pp (across 7 langs)",
            ha="center",
            va="top",
            fontsize=6.5,
            color="grey",
            transform=ax.transAxes,
        )

    axes[0][0].text(-0.05, 1.06, "gold", fontsize=7.5, ha="left", transform=axes[0][0].transAxes, color="grey")
    axes[0][0].text(1.0, 1.06, "predicted", fontsize=7.5, ha="right", transform=axes[0][0].transAxes, color="grey")

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["masculine"], label="masculine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["feminine"], label="feminine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["unknown"], label="unknown"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=8.5, bbox_to_anchor=(0.5, -0.02), frameon=False)
    fig.suptitle(
        "Where does each gold gender end up? (styles 1--4, masc/fem gold only, pooled over 7 languages)",
        fontsize=10.5,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = os.path.join(OUTPUT_DIR, "fig7_gender_flow_sankey.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 7 (alternative granularity): same flow diagram as
# figure_7_gender_flow_sankey, but for ONE model, one panel per LANGUAGE
# instead of one panel per model pooled over languages. Makes per-language
# variance directly visible as separate panels instead of a mean+-std
# annotation on a pooled ribbon -- exploratory, to compare against the
# pooled 6-model version before deciding which (or whether both) to keep.
# ---------------------------------------------------------------------------
def figure_7_gender_flow_sankey_by_language(model: str):
    node_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    gold_order = ("MASCULINE", "FEMININE")
    pred_order = ("MASCULINE", "FEMININE", "UNKNOWN")

    df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
    sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]

    fig, axes = plt.subplots(1, len(LANGUAGES), figsize=(2.1 * len(LANGUAGES), 3.4))
    for ax, lang in zip(axes, LANGUAGES):
        col = f"x_gender_{lang}"
        s = sub[sub[col].notna()]
        flows = {}
        for gold, pred in zip(s["x_gender"], s[col]):
            pred_bucket = pred if pred in ("MASCULINE", "FEMININE") else "UNKNOWN"
            flows[(gold, pred_bucket)] = flows.get((gold, pred_bucket), 0) + 1
        _draw_sankey_panel(ax, flows, gold_order, pred_order, node_colors)
        fem_err = (s[s["x_gender"] == "FEMININE"][col] != "FEMININE").mean() * 100
        masc_err = (s[s["x_gender"] == "MASCULINE"][col] != "MASCULINE").mean() * 100
        ax.set_title(f"{lang}\nfem {fem_err:.0f}% / masc {masc_err:.0f}%", fontsize=8.5)

    axes[0].text(-0.05, 1.14, "gold", fontsize=7, ha="left", transform=axes[0].transAxes, color="grey")
    axes[0].text(1.0, 1.14, "pred", fontsize=7, ha="right", transform=axes[0].transAxes, color="grey")

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["masculine"], label="masculine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["feminine"], label="feminine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["unknown"], label="unknown"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=8.5, bbox_to_anchor=(0.5, -0.05), frameon=False)
    fig.suptitle(
        f"{MODEL_LABELS[model]}: where does each gold gender end up, per language? (styles 1--4)",
        fontsize=10.5,
    )

    plt.tight_layout(rect=[0, 0.06, 1, 0.92])
    path = os.path.join(OUTPUT_DIR, f"fig7_gender_flow_sankey_by_language_{model}.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 7 (exploratory mega-grid): all 6 models stacked, one row each, same
# per-language panels as figure_7_gender_flow_sankey_by_language. Exploratory
# comparison view, not sized for the paper -- lets every model x language
# cell be inspected at once before deciding which single model's version (if
# any) is worth the space in the actual paper.
# ---------------------------------------------------------------------------
def figure_7_gender_flow_sankey_by_language_all_models():
    node_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    gold_order = ("MASCULINE", "FEMININE")
    pred_order = ("MASCULINE", "FEMININE", "UNKNOWN")

    fig, axes = plt.subplots(
        len(MODELS), len(LANGUAGES), figsize=(2.0 * len(LANGUAGES), 2.6 * len(MODELS))
    )
    for row, model in enumerate(MODELS):
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        for col_i, lang in enumerate(LANGUAGES):
            ax = axes[row][col_i]
            col = f"x_gender_{lang}"
            s = sub[sub[col].notna()]
            flows = {}
            for gold, pred in zip(s["x_gender"], s[col]):
                pred_bucket = pred if pred in ("MASCULINE", "FEMININE") else "UNKNOWN"
                flows[(gold, pred_bucket)] = flows.get((gold, pred_bucket), 0) + 1
            _draw_sankey_panel(ax, flows, gold_order, pred_order, node_colors)
            fem_err = (s[s["x_gender"] == "FEMININE"][col] != "FEMININE").mean() * 100
            masc_err = (s[s["x_gender"] == "MASCULINE"][col] != "MASCULINE").mean() * 100
            ax.set_title(f"{lang}: fem {fem_err:.0f}% / masc {masc_err:.0f}%", fontsize=7.5)
            if col_i == 0:
                ax.text(
                    -0.35, 0.5, MODEL_LABELS[model], fontsize=10, rotation=90,
                    va="center", ha="center", transform=ax.transAxes, fontweight="bold",
                )

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["masculine"], label="masculine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["feminine"], label="feminine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["unknown"], label="unknown"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=10, bbox_to_anchor=(0.5, -0.005), frameon=False)
    fig.suptitle(
        "All 6 systems x 7 languages: where does each gold gender end up? (styles 1--4)",
        fontsize=13,
    )

    plt.tight_layout(rect=[0.02, 0.015, 1, 0.97])
    path = os.path.join(OUTPUT_DIR, "fig7_gender_flow_sankey_by_language_ALL_MODELS.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# Romance (es/fr/it) and Slavic (ru/uk) grouped since they behave similarly
# throughout the paper; ar and he kept as their own single-language columns
# rather than merged into one "Semitic" group, since the two behave very
# differently (ar stays masculine-default, he frequently reverses).
LANGUAGE_FAMILIES = {
    "Romance (es/fr/it)": ["es", "fr", "it"],
    "Slavic (ru/uk)": ["ru", "uk"],
    "Arabic": ["ar"],
    "Hebrew": ["he"],
}


# ---------------------------------------------------------------------------
# Figure 7 (exploratory, language-family grouping): flows pooled by language
# family instead of individual language, for 3 selected systems (google,
# gpt-4o, systran) -- a 3x4 grid instead of the 6x7 mega-grid, to see if
# family-level grouping keeps the per-language story legible in less space.
# ---------------------------------------------------------------------------
def figure_7_gender_flow_sankey_by_family():
    node_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    gold_order = ("MASCULINE", "FEMININE")
    pred_order = ("MASCULINE", "FEMININE", "UNKNOWN")
    models = ["google", "gpt-4o", "systran"]
    families = list(LANGUAGE_FAMILIES.items())

    fig, axes = plt.subplots(len(models), len(families), figsize=(2.3 * len(families), 2.8 * len(models)))
    for row, model in enumerate(models):
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        for col_i, (family_name, langs) in enumerate(families):
            ax = axes[row][col_i]
            flows = {}
            fem_correct = fem_total = masc_correct = masc_total = 0
            fem_err_by_lang, masc_err_by_lang = [], []
            for lang in langs:
                col = f"x_gender_{lang}"
                s = sub[sub[col].notna()]
                for gold, pred in zip(s["x_gender"], s[col]):
                    pred_bucket = pred if pred in ("MASCULINE", "FEMININE") else "UNKNOWN"
                    flows[(gold, pred_bucket)] = flows.get((gold, pred_bucket), 0) + 1
                fem_s = s[s["x_gender"] == "FEMININE"]
                masc_s = s[s["x_gender"] == "MASCULINE"]
                fem_correct += (fem_s[col] == "FEMININE").sum()
                fem_total += len(fem_s)
                masc_correct += (masc_s[col] == "MASCULINE").sum()
                masc_total += len(masc_s)
                fem_err_by_lang.append((1 - (fem_s[col] == "FEMININE").mean()) * 100)
                masc_err_by_lang.append((1 - (masc_s[col] == "MASCULINE").mean()) * 100)
            _draw_sankey_panel(ax, flows, gold_order, pred_order, node_colors)
            fem_err = (1 - fem_correct / fem_total) * 100
            masc_err = (1 - masc_correct / masc_total) * 100
            # Std dev only meaningful for multi-language families (Romance,
            # Slavic); ar/he are single-language columns, so std is omitted
            # there rather than shown as a meaningless 0.
            if len(langs) > 1:
                fem_label = f"fem {fem_err:.0f}$\\pm${np.std(fem_err_by_lang):.0f}%"
                masc_label = f"masc {masc_err:.0f}$\\pm${np.std(masc_err_by_lang):.0f}%"
            else:
                fem_label = f"fem {fem_err:.0f}%"
                masc_label = f"masc {masc_err:.0f}%"
            ax.set_title(f"{family_name}\n{fem_label} / {masc_label}", fontsize=8.5)
            if col_i == 0:
                ax.text(
                    -0.4, 0.5, MODEL_LABELS[model], fontsize=11, rotation=90,
                    va="center", ha="center", transform=ax.transAxes, fontweight="bold",
                )

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["masculine"], label="masculine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["feminine"], label="feminine"),
        plt.Rectangle((0, 0), 1, 1, color=GENDER_COLORS["unknown"], label="unknown"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=9, bbox_to_anchor=(0.5, -0.01), frameon=False)
    fig.suptitle(
        "Google / GPT-4o / SYSTRAN, pooled by language family: where does each gold gender end up?",
        fontsize=11.5,
    )

    plt.tight_layout(rect=[0.03, 0.02, 1, 0.95])
    path = os.path.join(OUTPUT_DIR, "fig7_gender_flow_sankey_by_family.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 7: error rate by gold gender, per system, averaged over 7 languages.
# Directly from outputs/<model>/<model>_confusion_metrics.csv (already
# computed, FEMININE_recall / MASCULINE_recall per language) -- error rate
# = 1 - recall. No new computation, just a dedicated chart for a number that
# was previously only mentioned in text.
# ---------------------------------------------------------------------------
def figure_7_error_rate_by_gender():
    # DIVERSE deliberately left out again: its error rate (~98-99% flat
    # across every system) is already the fully-reported 1.2 headline
    # finding in the text, and visually it dwarfed the feminine/masculine
    # bars -- which are the actual comparison this figure is about --
    # without adding anything the text numbers don't already say.
    #
    # "Error rate" here = 1 - recall, where recall (for e.g. "feminine") is:
    # of all instances whose GOLD (correct) gender is feminine, what
    # fraction did the system output as feminine? So error rate = the
    # fraction of truly-feminine instances the system got wrong (output
    # as masculine, neuter, or unknown instead) -- not the overall
    # error rate of the system.
    fem_err, masc_err = [], []
    fem_std, masc_std = [], []
    for model in MODELS:
        df = pd.read_csv(f"outputs/{model}/{model}_confusion_metrics.csv", index_col=0)
        fem_recall = df.loc["FEMININE_recall"].astype(float)
        masc_recall = df.loc["MASCULINE_recall"].astype(float)
        fem_err.append((1 - fem_recall.mean()) * 100)
        masc_err.append((1 - masc_recall.mean()) * 100)
        # Std dev across the 7 languages, per gender -- shown as error bars
        # so it's visible whether the pooled asymmetry is consistent across
        # languages or driven by one or two extreme ones.
        fem_std.append(((1 - fem_recall) * 100).std())
        masc_std.append(((1 - masc_recall) * 100).std())

    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    x = np.arange(len(MODELS))
    w = 0.35
    errkw = dict(ecolor="black", elinewidth=0.8, capsize=2.5, capthick=0.8)
    ax.bar(
        x - w / 2,
        fem_err,
        width=w,
        yerr=fem_std,
        color=GENDER_COLORS["feminine"],
        label="feminine (gold)",
        edgecolor="white",
        error_kw=errkw,
    )
    ax.bar(
        x + w / 2,
        masc_err,
        width=w,
        yerr=masc_std,
        color=GENDER_COLORS["masculine"],
        label="masculine (gold)",
        edgecolor="white",
        error_kw=errkw,
    )
    for i in range(len(MODELS)):
        ax.text(
            x[i] - w / 2,
            fem_err[i] + fem_std[i] + 1,
            f"{fem_err[i]:.0f}%",
            ha="center",
            fontsize=6.5,
            color=GENDER_COLORS["feminine"],
        )
        ax.text(
            x[i] + w / 2,
            masc_err[i] + masc_std[i] + 1,
            f"{masc_err[i]:.0f}%",
            ha="center",
            fontsize=6.5,
            color=GENDER_COLORS["masculine"],
        )

    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], rotation=25, ha="right", fontsize=7.5)
    ax.set_ylabel("Error rate (%)\n(share of gold-feminine/masculine\ninstances translated with the wrong gender)", fontsize=7.5)
    ax.set_ylim(0, max(fem_err) + max(fem_std) + 12)
    ax.set_title("How often is each gender mistranslated?\n(averaged over 7 languages)", fontsize=9)
    # No inside corner is reliably free: the feminine error bars are tall
    # enough at most models (DeepL/Microsoft/SYSTRAN reach ~75-83%) that an
    # inside legend collided with one of them regardless of corner. Legend
    # goes outside the axes on the right instead.
    fig.subplots_adjust(right=0.78)
    fig.legend(
        *ax.get_legend_handles_labels(),
        fontsize=7.5,
        loc="center left",
        bbox_to_anchor=(0.8, 0.5),
        frameon=True,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

    path = os.path.join(OUTPUT_DIR, "fig7_error_rate_by_gender.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 7b: same fem/masc/diverse error rate as figure 7, but x-axis =
# language instead of system (pooled over 6 systems this time, std dev
# across systems as error bars) -- companion view for whether the asymmetry
# is a property of the target language rather than (or in addition to) the
# MT system.
# ---------------------------------------------------------------------------
def figure_7b_error_rate_by_language():
    fem_err, masc_err, div_err = [], [], []
    fem_std, masc_std, div_std = [], [], []
    for j, lang in enumerate(LANGUAGES):
        fem_vals, masc_vals, div_vals = [], [], []
        for model in MODELS:
            df = pd.read_csv(f"outputs/{model}/{model}_confusion_metrics.csv", index_col=0)
            col = str(j)
            fem_vals.append((1 - float(df.loc["FEMININE_recall", col])) * 100)
            masc_vals.append((1 - float(df.loc["MASCULINE_recall", col])) * 100)
            div_vals.append((1 - float(df.loc["DIVERSE_recall", col])) * 100)
        fem_err.append(np.mean(fem_vals))
        masc_err.append(np.mean(masc_vals))
        div_err.append(np.mean(div_vals))
        fem_std.append(np.std(fem_vals))
        masc_std.append(np.std(masc_vals))
        div_std.append(np.std(div_vals))

    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    x = np.arange(len(LANGUAGES))
    w = 0.26
    errkw = dict(ecolor="black", elinewidth=0.8, capsize=2.5, capthick=0.8)
    ax.bar(
        x - w,
        fem_err,
        width=w,
        yerr=fem_std,
        color=GENDER_COLORS["feminine"],
        label="feminine (gold)",
        edgecolor="white",
        error_kw=errkw,
    )
    ax.bar(
        x,
        masc_err,
        width=w,
        yerr=masc_std,
        color=GENDER_COLORS["masculine"],
        label="masculine (gold)",
        edgecolor="white",
        error_kw=errkw,
    )
    ax.bar(
        x + w,
        div_err,
        width=w,
        yerr=div_std,
        color=GENDER_COLORS["diverse"],
        label="diverse (gold)",
        edgecolor="white",
        error_kw=errkw,
    )
    for i in range(len(LANGUAGES)):
        fem_y = fem_err[i] + fem_std[i] + 1
        masc_y = masc_err[i] + masc_std[i] + 1
        div_y = div_err[i] + div_std[i] + 1
        # he's feminine/masculine bars land at nearly the same height (this
        # is the Hebrew reversal), which put their labels close enough to
        # visually merge ("20%31%") despite being on separate bars -- push
        # them apart vertically whenever they'd land within 5pp of each other.
        if abs(fem_y - masc_y) < 5:
            if masc_y >= fem_y:
                masc_y = fem_y + 5
            else:
                masc_y = fem_y - 5
        ax.text(
            x[i] - w, fem_y, f"{fem_err[i]:.0f}%", ha="center", fontsize=6, color=GENDER_COLORS["feminine"]
        )
        ax.text(
            x[i], masc_y, f"{masc_err[i]:.0f}%", ha="center", fontsize=6, color=GENDER_COLORS["masculine"]
        )
        ax.text(
            x[i] + w, div_y, f"{div_err[i]:.0f}%", ha="center", fontsize=6, color=GENDER_COLORS["diverse"]
        )

    ax.set_xticks(x)
    ax.set_xticklabels(LANGUAGES, fontsize=8.5)
    ax.set_ylabel("Error rate (%)\n(1 - recall for that gender)", fontsize=8)
    ax.set_ylim(0, max(div_err) + max(div_std) + 15)
    ax.set_title("How often is each gender mistranslated?\n(averaged over 6 systems)", fontsize=9)

    fig.subplots_adjust(right=0.8)
    fig.legend(
        *ax.get_legend_handles_labels(),
        fontsize=7,
        loc="center left",
        bbox_to_anchor=(0.81, 0.5),
        frameon=True,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

    path = os.path.join(OUTPUT_DIR, "fig7b_error_rate_by_language.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 8: neutral-name results, split into the 3 scenarios that
# templates.py::gen_for_xs actually generates -- gold is NOT always
# ambiguous just because the name is: neutral name + masculine-form job
# (gold=MASCULINE), + feminine-form job (gold=FEMININE), and + DIVERSE-form
# job (gold=DIVERSE, the only case where "neutral" is actually the correct
# answer). Stacked prediction distribution per language, pooled over the
# 5 available systems (GPT-4o pending background translation).
# ---------------------------------------------------------------------------
def figure_8_neutral_name_scenarios():
    scenarios = [
        ("MASCULINE", "Neutral name + masculine-form job\n(correct answer: masculine)"),
        ("FEMININE", "Neutral name + feminine-form job\n(correct answer: feminine)"),
        ("DIVERSE", "Neutral name + DIVERSE-form job\n(correct answer: neutral)"),
    ]
    pred_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "NEUTER": GENDER_COLORS["neuter"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    models = MODELS
    # Stack order puts the correct answer for that panel's gold value at the
    # bottom of the bar (masculine-form job -> blue at bottom, feminine-form
    # -> orange at bottom, DIVERSE-form -> neuter/green at bottom, since
    # NEUTER is the closest achievable proxy for DIVERSE).
    stack_orders = {
        "MASCULINE": ["MASCULINE", "FEMININE", "NEUTER", "UNKNOWN"],
        "FEMININE": ["FEMININE", "MASCULINE", "NEUTER", "UNKNOWN"],
        "DIVERSE": ["NEUTER", "MASCULINE", "FEMININE", "UNKNOWN"],
    }

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.2), sharey=True)

    for ax, (gold_value, title) in zip(axes, scenarios):
        counts_by_lang = {
            lang: {"MASCULINE": 0, "FEMININE": 0, "NEUTER": 0, "UNKNOWN": 0} for lang in LANGUAGES
        }
        for model in models:
            df = pd.read_csv(
                f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";"
            )
            sub = df[
                (df["sentence_style"] == 6)
                & (df["name_gender"] == "n")
                & (df["x_gender"] == gold_value)
            ]
            for lang in LANGUAGES:
                col = f"x_gender_{lang}"
                if col not in sub.columns:
                    continue
                for pred, count in sub[col].value_counts().items():
                    if pred in counts_by_lang[lang]:
                        counts_by_lang[lang][pred] += count

        bottoms = np.zeros(len(LANGUAGES))
        for pred_type in stack_orders[gold_value]:
            vals = []
            for lang in LANGUAGES:
                total = sum(counts_by_lang[lang].values()) or 1
                vals.append(counts_by_lang[lang][pred_type] / total * 100)
            ax.bar(LANGUAGES, vals, bottom=bottoms, color=pred_colors[pred_type])
            bottoms += np.array(vals)

        ax.set_title(title, fontsize=8)
        ax.tick_params(labelsize=7.5)

    axes[0].set_ylabel("% of predictions", fontsize=8)
    # Fixed legend order (Masculine/Feminine/Neuter/Unknown) regardless of
    # which panel's stack order happens to be drawn last -- relying on
    # axes[-1]'s own draw order made the legend order flip depending on
    # that panel's gold value (DIVERSE panels draw Neuter first).
    legend_order = ["MASCULINE", "FEMININE", "NEUTER", "UNKNOWN"]
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=pred_colors[p], label=p.title()) for p in legend_order
    ]
    axes[-1].legend(
        handles=legend_handles,
        fontsize=7,
        loc="upper left",
        bbox_to_anchor=(1.0, 1.0),
        title="Predicted",
        title_fontsize=7.5,
    )
    # Single suptitle with the caveat as a smaller second line via \n --
    # a separate fig.text() near the suptitle collided with it (both sat at
    # nearly the same y), and \n keeps their vertical spacing consistent
    # regardless of figure size.
    fig.suptitle(
        "Neutral names: what gets predicted, by what the correct answer actually is\n"
        "pooled over all 6 systems",
        fontsize=9.5,
    )

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig8_neutral_name_scenarios.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 9: does an unambiguous name (vs. a neutral/ambiguous one) change how
# a matching-form job noun gets translated -- side by side for both the
# masculine and the feminine case, so the neutral-vs-named comparison AND
# the masculine-vs-feminine comparison are both visible in one figure.
# NB: the dataset never pairs a name with the "wrong" job-form gender (a
# masculine name only ever appears with a masculine-form or DIVERSE-form
# job, never a feminine-form one), so a masc-name-vs-fem-job panel isn't
# possible here -- deliberately scoped to the 4 pairs that actually exist.
# ---------------------------------------------------------------------------
def figure_9_name_gender_effect():
    # 2x2 grid: left column = masculine-form job (named on top, neutral
    # below), right column = feminine-form job (named on top, neutral
    # below) -- keeps the "does a name help, relative to neutral" comparison
    # stacked vertically within each column, and the masculine-vs-feminine
    # comparison side by side across columns.
    grid = [
        [("MASCULINE", "MASCULINE", "Masculine name\n+ masculine-form job"),
         ("FEMININE", "FEMININE", "Feminine name\n+ feminine-form job")],
        [("n", "MASCULINE", "Neutral name\n+ masculine-form job"),
         ("n", "FEMININE", "Neutral name\n+ feminine-form job")],
    ]
    pred_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "NEUTER": GENDER_COLORS["neuter"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    # Correct answer's color goes at the bottom of the stack, matching
    # figure 8's convention.
    stack_orders = {
        "MASCULINE": ["MASCULINE", "FEMININE", "NEUTER", "UNKNOWN"],
        "FEMININE": ["FEMININE", "MASCULINE", "NEUTER", "UNKNOWN"],
    }
    models = MODELS

    # sharex=True would hide the language tick labels on the top row --
    # each panel needs its own, they're not a continuous shared axis.
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 6.0), sharey=True)

    for row in range(2):
        for col in range(2):
            ax = axes[row][col]
            name_gender, job_gender, title = grid[row][col]
            counts_by_lang = {
                lang: {"MASCULINE": 0, "FEMININE": 0, "NEUTER": 0, "UNKNOWN": 0}
                for lang in LANGUAGES
            }
            for model in models:
                df = pd.read_csv(
                    f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";"
                )
                sub = df[
                    (df["sentence_style"] == 6)
                    & (df["name_gender"] == name_gender)
                    & (df["x_gender"] == job_gender)
                ]
                for lang in LANGUAGES:
                    col_name = f"x_gender_{lang}"
                    if col_name not in sub.columns:
                        continue
                    for pred, count in sub[col_name].value_counts().items():
                        if pred in counts_by_lang[lang]:
                            counts_by_lang[lang][pred] += count

            bottoms = np.zeros(len(LANGUAGES))
            for pred_type in stack_orders[job_gender]:
                vals = []
                for lang in LANGUAGES:
                    total = sum(counts_by_lang[lang].values()) or 1
                    vals.append(counts_by_lang[lang][pred_type] / total * 100)
                ax.bar(LANGUAGES, vals, bottom=bottoms, color=pred_colors[pred_type])
                bottoms += np.array(vals)

            ax.set_title(title, fontsize=8.5)
            ax.tick_params(labelsize=7.5)

    axes[0][0].set_ylabel("% of predictions", fontsize=8)
    axes[1][0].set_ylabel("% of predictions", fontsize=8)
    legend_order = ["MASCULINE", "FEMININE", "NEUTER", "UNKNOWN"]
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=pred_colors[p], label=p.title()) for p in legend_order
    ]
    axes[0][1].legend(
        handles=legend_handles,
        fontsize=7,
        loc="upper left",
        bbox_to_anchor=(1.0, 1.0),
        title="Predicted",
        title_fontsize=7.5,
    )
    fig.suptitle(
        "Does an unambiguous name change translation of a matching-form job,\n"
        "compared to a neutral name? pooled over all 6 systems",
        fontsize=9.5,
    )

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig9_name_gender_effect.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Figure 10: when a DIVERSE (dey-pronoun) subject in a romantic-partner
# sentence (style 5) isn't translated as neutral, which direction does it get
# mistranslated in, and does that depend on the partner's (binary) gender?
# It doesn't (checked separately: NEUTER-rate is ~1% regardless of partner
# gender, chi2 p=0.69, no heteronormativity-style effect here) -- so this
# figure pools over partner gender and shows the per-language misdirection
# instead, which DOES vary a lot: mostly a feminine default (es 74%, he 79%),
# but ar flips to masculine (47% vs 25%) -- the opposite of the masculine-
# default pattern seen elsewhere in the paper (e.g. figure 4's neutral names).
# ---------------------------------------------------------------------------
def figure_10_diverse_romantic_misdirection():
    pred_colors = {
        "MASCULINE": GENDER_COLORS["masculine"],
        "FEMININE": GENDER_COLORS["feminine"],
        "NEUTER": GENDER_COLORS["neuter"],
        "UNKNOWN": GENDER_COLORS["unknown"],
    }
    models = ["google", "google_llm", "deepl", "microsoft", "systran"]  # gpt-4o pending

    counts_by_lang = {
        lang: {"MASCULINE": 0, "FEMININE": 0, "NEUTER": 0, "UNKNOWN": 0} for lang in LANGUAGES
    }
    for model in models:
        df = pd.read_csv(
            f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";"
        )
        sub = df[(df["sentence_style"] == 5) & (df["x_gender"] == "DIVERSE")]
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            if col not in sub.columns:
                continue
            for pred, count in sub[col].value_counts().items():
                if pred in counts_by_lang[lang]:
                    counts_by_lang[lang][pred] += count

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    bottoms = np.zeros(len(LANGUAGES))
    for pred_type in ["FEMININE", "MASCULINE", "NEUTER", "UNKNOWN"]:
        vals = []
        for lang in LANGUAGES:
            total = sum(counts_by_lang[lang].values()) or 1
            vals.append(counts_by_lang[lang][pred_type] / total * 100)
        ax.bar(LANGUAGES, vals, bottom=bottoms, color=pred_colors[pred_type], label=pred_type.title())
        bottoms += np.array(vals)

    ax.set_ylabel("% of predictions", fontsize=8)
    ax.set_ylim(0, 100)
    ax.tick_params(labelsize=8.5)
    ax.set_title(
        "DIVERSE subject in romantic-partner sentences:\nwhat gets predicted instead? (partner gender pooled: no effect)",
        fontsize=9,
    )
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.0, 1.0), title="Predicted", title_fontsize=7.5)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig10_diverse_romantic_misdirection.pdf")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print("Saved", path)


# ---------------------------------------------------------------------------
# Verification: independently recompute every numeric claim in main.tex
# directly from processed_data/, deliberately NOT reusing the figure/table
# helpers above (load_binary_dataset, _binary_accuracy_by_style, etc.) -- the
# point is a from-scratch cross-check, so a bug shared between the figure
# code and this code can't silently agree with itself. Each function prints
# to console and writes a CSV to OUTPUT_DIR so every claim has a paper-trail.
# ---------------------------------------------------------------------------
def verify_dataset_counts():
    rows = []
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        rows.append({"model": model, "n_sentences": len(df), "dataset": "main (styles 1-4)"})
        rdf = pd.read_csv(f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";")
        rows.append({"model": model, "n_sentences": len(rdf), "dataset": "romantic/names (styles 5-6)"})
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_dataset_counts.csv")
    out.to_csv(csv_path, index=False)
    print(out.to_string(index=False))
    print("Saved", csv_path)
    return out


def verify_main_evaluation():
    rows = []
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            preds = sub[col].dropna()
            gold = sub.loc[preds.index, "x_gender"]
            correct = (preds == gold).sum()
            total = len(preds)
            rows.append(
                {
                    "model": model,
                    "language": lang,
                    "n": total,
                    "accuracy_pct": round(correct / total * 100, 1) if total else None,
                }
            )
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_main_evaluation_accuracy.csv")
    out.to_csv(csv_path, index=False)

    gpt4o = out[out["model"] == "gpt-4o"]["accuracy_pct"]
    trad = out[out["model"] != "gpt-4o"]["accuracy_pct"]
    print(f"GPT-4o range: {gpt4o.min()}--{gpt4o.max()}")
    print(f"Traditional systems range: {trad.min()}--{trad.max()}")

    piv = out.pivot(index="language", columns="model", values="accuracy_pct")
    diff = (piv["google"] - piv["google_llm"]).abs()
    print(f"Google vs Google-LLM max abs diff: {diff.max():.2f}pp")

    err_rows = []
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        sub = df[df["sentence_style"].isin([1, 2, 3, 4]) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            errs = sub[sub[col].notna() & (sub[col] != sub["x_gender"]) & sub[col].isin(["MASCULINE", "FEMININE"])]
            f_to_m = ((errs["x_gender"] == "FEMININE") & (errs[col] == "MASCULINE")).sum()
            m_to_f = ((errs["x_gender"] == "MASCULINE") & (errs[col] == "FEMININE")).sum()
            err_rows.append({"model": model, "language": lang, "fem_to_masc": f_to_m, "masc_to_fem": m_to_f})
    err_out = pd.DataFrame(err_rows)
    err_csv = os.path.join(OUTPUT_DIR, "verify_error_direction.csv")
    err_out.to_csv(err_csv, index=False)
    n_fm_dominant = (err_out["fem_to_masc"] >= err_out["masc_to_fem"]).sum()
    print(f"fem->masc >= masc->fem in {n_fm_dominant}/{len(err_out)} model-language cells")
    print("Saved", csv_path, "and", err_csv)
    return out


def verify_trans_identity():
    def acc(df, style):
        sub = df[(df["sentence_style"] == style) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        rows = {}
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            preds = sub[col].dropna()
            gold = sub.loc[preds.index, "x_gender"]
            rows[lang] = round((preds == gold).mean() * 100, 1) if len(preds) else None
        return rows

    rows = []
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        base = acc(df, 1)
        trans = acc(df, 3)
        for lang in LANGUAGES:
            rows.append(
                {
                    "model": model,
                    "language": lang,
                    "baseline_style1_pct": base[lang],
                    "trans_style3_pct": trans[lang],
                    "delta_pp": round(trans[lang] - base[lang], 1) if base[lang] and trans[lang] else None,
                }
            )
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_trans_identity.csv")
    out.to_csv(csv_path, index=False)
    n_improved = (out["delta_pp"] > 0).sum()
    print(f"Trans-marked improves over baseline in {n_improved}/{len(out)} model-language cells")
    print("Saved", csv_path)
    return out


def verify_pronoun_elaboration():
    def acc_pooled(df, style):
        sub = df[(df["sentence_style"] == style) & df["x_gender"].isin(["MASCULINE", "FEMININE"])]
        correct = total = 0
        for lang in LANGUAGES:
            col = f"x_gender_{lang}"
            preds = sub[col].dropna()
            gold = sub.loc[preds.index, "x_gender"]
            correct += (preds == gold).sum()
            total += len(preds)
        return round(correct / total * 100, 1) if total else None

    rows = []
    for model in MODELS:
        df = pd.read_csv(f"processed_data/avg_DEval/{model}_processed.csv", sep=";")
        s1 = acc_pooled(df, 1)
        s2 = acc_pooled(df, 2)
        rows.append(
            {
                "model": model,
                "style1_baseline_pooled_pct": s1,
                "style2_pronoun_pooled_pct": s2,
                "delta_pp": round(s2 - s1, 1),
            }
        )
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_pronoun_elaboration.csv")
    out.to_csv(csv_path, index=False)
    print(out.to_string(index=False))
    print("Saved", csv_path)
    return out


def verify_names():
    sig_rows = []
    for lang in LANGUAGES:
        pooled_errors = []
        for model in MODELS:
            df = pd.read_csv(f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";")
            sub = df[(df["sentence_style"] == 6) & (df["name_gender"] == "n")]
            col = f"x_gender_{lang}"
            if col not in sub.columns:
                continue
            pooled_errors.extend(
                (g, p)
                for g, p in zip(sub["x_gender"], sub[col])
                if pd.notna(p) and g != p and p in ("MASCULINE", "FEMININE")
            )
        result = test_direction_skew(pooled_errors)
        result["language"] = lang
        sig_rows.append(result)
    sig_out = pd.DataFrame(sig_rows)
    sig_csv = os.path.join(OUTPUT_DIR, "verify_names_error_direction_significance.csv")
    sig_out.to_csv(sig_csv, index=False)
    print(sig_out.to_string(index=False))

    def acc(name_gender, job_gender):
        correct = total = 0
        for model in MODELS:
            df = pd.read_csv(f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";")
            sub = df[
                (df["sentence_style"] == 6) & (df["name_gender"] == name_gender) & (df["x_gender"] == job_gender)
            ]
            for lang in LANGUAGES:
                col = f"x_gender_{lang}"
                if col not in sub.columns:
                    continue
                preds = sub[col].dropna()
                total += len(preds)
                correct += (preds == job_gender).sum()
        return round(correct / total * 100, 1) if total else None, correct, total

    effect_rows = []
    for ng, jg, label in [
        ("MASCULINE", "MASCULINE", "masc_name+masc_job"),
        ("n", "MASCULINE", "neutral_name+masc_job"),
        ("FEMININE", "FEMININE", "fem_name+fem_job"),
        ("n", "FEMININE", "neutral_name+fem_job"),
    ]:
        a, c, t = acc(ng, jg)
        effect_rows.append({"scenario": label, "accuracy_pct": a, "correct": c, "total": t})
    effect_out = pd.DataFrame(effect_rows)
    effect_csv = os.path.join(OUTPUT_DIR, "verify_name_gender_effect.csv")
    effect_out.to_csv(effect_csv, index=False)
    print(effect_out.to_string(index=False))
    print("Saved", sig_csv, "and", effect_csv)
    return sig_out, effect_out


def verify_heteronormativity():
    """Independent cross-check of table_heteronormativity_gap() above -- same
    computation, written from scratch against raw processed_data/ instead of
    going through that function, so a shared bug can't agree with itself.
    Uses test_paired_gap (McNemar), matching the paired design: every
    subject sentence is generated with both a same-gender and a different-
    gender partner, so the two conditions are matched pairs, not independent
    samples."""
    rows = []
    for lang in LANGUAGES:
        correct_diff, correct_same = [], []
        for model in MODELS:
            df = pd.read_csv(f"processed_data/romantic_names/romantic_name_{model}_processed.csv", sep=";")
            sub = df[df["sentence_style"] == 5]
            col = f"x_gender_{lang}"
            if col not in sub.columns:
                continue
            binary = sub[
                sub["x_gender"].isin(["MASCULINE", "FEMININE"])
                & sub["y_gender"].isin(["MASCULINE", "FEMININE"])
                & sub[col].notna()
            ].copy()
            binary["correct"] = binary["x_gender"] == binary[col]
            binary["pairing"] = np.where(binary["x_gender"] == binary["y_gender"], "same", "diff")
            piv = binary.pivot_table(
                index=["sentence_id", "x_nom_sg", "x_gender"], columns="pairing", values="correct", aggfunc="first"
            ).dropna()
            correct_diff.extend(piv["diff"].tolist())
            correct_same.extend(piv["same"].tolist())
        result = test_paired_gap(correct_diff, correct_same)
        rows.append(
            {
                "language": lang,
                "n": result["n"],
                "n_discordant": result["n_discordant"],
                "hetero_accuracy_pct": round(result["accuracy_a"] * 100, 2),
                "same_gender_accuracy_pct": round(result["accuracy_b"] * 100, 2),
                "gap_pp": round((result["accuracy_a"] - result["accuracy_b"]) * 100, 2),
                "p_value": result["p_value"],
            }
        )
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_heteronormativity_gap.csv")
    out.to_csv(csv_path, index=False)
    print(out.to_string(index=False))
    print("Saved", csv_path, "-- compare against table_heteronormativity_gap.csv")
    return out


def verify_stereotypicality():
    """Sanity check only: does accuracy trend monotonically with per-instance
    stereotype-congruence (x_stereotypical), GPT-4o? Not a refit of the
    logistic regression in table_logistic_regression -- just confirms the
    direction (and Hebrew's reversal) independently."""
    df = pd.read_csv("processed_data/avg_DEval/gpt-4o_processed.csv", sep=";")
    sub = df[
        df["sentence_style"].isin([1, 2, 3, 4])
        & df["x_gender"].isin(["MASCULINE", "FEMININE"])
        & df["x_stereotypical"].notna()
    ].copy()
    sub["decile"] = pd.qcut(sub["x_stereotypical"], 10, labels=False, duplicates="drop")
    rows = []
    for lang in LANGUAGES:
        col = f"x_gender_{lang}"
        for decile, group in sub.groupby("decile"):
            preds = group[col].dropna()
            gold = group.loc[preds.index, "x_gender"]
            rows.append(
                {
                    "language": lang,
                    "stereotypicality_decile": decile,
                    "n": len(preds),
                    "accuracy_pct": round((preds == gold).mean() * 100, 1) if len(preds) else None,
                }
            )
    out = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "verify_stereotypicality_by_decile.csv")
    out.to_csv(csv_path, index=False)

    corr_rows = []
    for lang in LANGUAGES:
        lang_df = out[out["language"] == lang].dropna()
        corr = lang_df["stereotypicality_decile"].corr(lang_df["accuracy_pct"], method="spearman")
        corr_rows.append({"language": lang, "spearman_corr_decile_vs_accuracy": round(corr, 3)})
    corr_out = pd.DataFrame(corr_rows)
    corr_csv = os.path.join(OUTPUT_DIR, "verify_stereotypicality_monotonicity.csv")
    corr_out.to_csv(corr_csv, index=False)
    print(corr_out.to_string(index=False))
    print("Saved", csv_path, "and", corr_csv)
    return out, corr_out


if __name__ == "__main__":
    # Dropped from the default pipeline (still callable manually if needed):
    # figure_4_diverging_bias (redundant with figure_8_neutral_name_scenarios),
    # figure_5_stereotypicality_scatter (table_logistic_regression covers the
    # same finding with exact numbers), figure_7_error_rate_by_gender /
    # figure_7_gender_flow_sankey (pooled 6-model versions of the fig7 story --
    # exploratory steps on the way to figure_7_gender_flow_sankey_by_family,
    # which is the one actually used: fewer systems (google/gpt-4o/systran)
    # but per-language-family granularity plus std dev, which the pooled
    # 6-model version couldn't show without a separate mean+-std annotation),
    # figure_7_gender_flow_sankey_by_language (single-model, single-language
    # granularity -- superseded by the family-grouped version, which is a
    # good middle ground), figure_7_gender_flow_sankey_by_language_all_models
    # (6x7 mega-grid, exploratory only, too dense for the paper),
    # figure_7b_error_rate_by_language (redundant with figure_7, transposed),
    # figure_8_neutral_name_scenarios (cut for space -- error-direction
    # significance already reported as text in the Names section),
    # figure_10_diverse_romantic_misdirection (interesting but tangential --
    # cut for space).
    figure_1_accuracy_heatmap()
    figure_2_occupation_scatter()
    figure_3_context_effects()
    table_heteronormativity_gap()
    table_logistic_regression()
    table_human_eval_agreement()
    table_human_eval_by_model()
    print_alignment_match_rate()
    print_winomt_style_agreement()
    print_human_eval_reliability_baseline()
    figure_7_gender_flow_sankey_by_family()
    figure_9_name_gender_effect()

    # Independent from-scratch verification of every numeric claim in main.tex.
    verify_dataset_counts()
    verify_main_evaluation()
    verify_trans_identity()
    verify_pronoun_elaboration()
    verify_names()
    verify_heteronormativity()
    verify_stereotypicality()
