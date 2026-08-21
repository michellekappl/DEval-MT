import pandas as pd


def compare_accuracy_by_language(
    accuracies_a: dict[str, dict[str, float]],
    accuracies_b: dict[str, dict[str, float]],
    label_a: str,
    label_b: str,
) -> pd.DataFrame:
    """Compare per-language accuracy between two conditions (e.g. two sentence
    styles, or two systems), given as {group: {language: accuracy}} -- group
    is typically a model/system name, but can be any grouping key.

    Returns one row per (group, language) present in both inputs, with both
    accuracies and the percentage-point difference (b - a).
    """
    rows = []
    for group in accuracies_a:
        if group not in accuracies_b:
            continue
        acc_a = accuracies_a[group]
        acc_b = accuracies_b[group]
        for lang in acc_a:
            if lang not in acc_b:
                continue
            rows.append(
                {
                    "model": group,
                    "language": lang,
                    f"accuracy_{label_a}": acc_a[lang],
                    f"accuracy_{label_b}": acc_b[lang],
                    "diff_pp": (acc_b[lang] - acc_a[lang]) * 100,
                }
            )
    return pd.DataFrame(rows)
