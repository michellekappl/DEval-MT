"""Significance tests for gender bias evaluation.

Three question types, three tests:
- test_direction_skew: does a single sample's error direction deviate from a
  theoretically motivated 50/50 split? -> exact binomial test (not a chi-square
  goodness-of-fit approximation, since some cells are small/extreme, e.g. 3/174).
- test_group_gap: does accuracy differ between two INDEPENDENT groups on a
  categorical (correct/incorrect) outcome, with no natural 1:1 correspondence
  between an item in group A and an item in group B? -> chi-square test of
  independence on a 2x2 contingency table (equivalent to a two-proportion
  test). Not a t-test (outcome isn't continuous).
- test_paired_gap: does accuracy differ between two PAIRED/matched conditions
  measured on the same underlying item (e.g. the same subject sentence, once
  with a same-gender romantic partner and once with a different-gender
  partner -- the dataset generates both for every subject)? -> McNemar's
  test, using only the discordant pairs. More powerful than test_group_gap
  when a natural pairing exists, since it removes item-level noise instead
  of treating the two conditions as independent samples.
"""

from scipy.stats import binomtest, chi2_contingency
from statsmodels.stats.contingency_tables import mcnemar


def test_direction_skew(
    errors: list[tuple[str, str]],
    direction_a: str = "MASCULINE",
    direction_b: str = "FEMININE",
) -> dict:
    """Binomial test: among misclassifications, is one error direction
    significantly more common than the other, vs. an expected 50/50 split?

    Parameters
    ----------
    errors : list of (gold, pred) tuples, already filtered to gold != pred.
    direction_a, direction_b : the two wrong-prediction values to compare.
    """
    n_a = sum(1 for _, pred in errors if pred == direction_a)
    n_b = sum(1 for _, pred in errors if pred == direction_b)
    n = n_a + n_b
    if n == 0:
        return {"n": 0, "p_value": None, "skew_toward": None}

    result = binomtest(n_a, n, 0.5)
    return {
        "n": n,
        f"n_{direction_a}": n_a,
        f"n_{direction_b}": n_b,
        "skew_toward": direction_a if n_a > n_b else direction_b,
        "p_value": result.pvalue,
    }


def test_group_gap(
    group_a: list[tuple[str, str]],
    group_b: list[tuple[str, str]],
) -> dict:
    """Chi-square test of independence: does accuracy differ between two
    independent groups of (gold, pred) pairs, e.g. same-gender-pair vs.
    different-gender-pair sentences?
    """
    a_correct = sum(1 for g, p in group_a if g == p)
    a_wrong = len(group_a) - a_correct
    b_correct = sum(1 for g, p in group_b if g == p)
    b_wrong = len(group_b) - b_correct

    table = [[a_correct, a_wrong], [b_correct, b_wrong]]
    chi2, p_value, dof, expected = chi2_contingency(table)

    return {
        "n_a": len(group_a),
        "n_b": len(group_b),
        "accuracy_a": a_correct / len(group_a) if group_a else None,
        "accuracy_b": b_correct / len(group_b) if group_b else None,
        "chi2": chi2,
        "p_value": p_value,
    }


def test_paired_gap(
    correct_a: list[bool],
    correct_b: list[bool],
) -> dict:
    """McNemar's test (continuity-corrected): does accuracy differ between
    two paired conditions measured on the same underlying item?

    Parameters
    ----------
    correct_a, correct_b : parallel lists of booleans -- correct_a[i] and
        correct_b[i] must be the two conditions' outcomes for the SAME item i
        (e.g. the same subject sentence under a same-gender vs. a different-
        gender partner). Must be the same length and aligned by item.
    """
    n = len(correct_a)
    both_correct = sum(1 for a, b in zip(correct_a, correct_b) if a and b)
    a_only = sum(1 for a, b in zip(correct_a, correct_b) if a and not b)
    b_only = sum(1 for a, b in zip(correct_a, correct_b) if not a and b)
    both_wrong = sum(1 for a, b in zip(correct_a, correct_b) if not a and not b)

    table = [[both_correct, a_only], [b_only, both_wrong]]
    result = mcnemar(table, exact=False, correction=True)

    return {
        "n": n,
        "n_discordant": a_only + b_only,
        "accuracy_a": sum(correct_a) / n if n else None,
        "accuracy_b": sum(correct_b) / n if n else None,
        "statistic": result.statistic,
        "p_value": result.pvalue,
    }
