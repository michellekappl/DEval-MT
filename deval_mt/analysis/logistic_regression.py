"""Logistic Regression Analysis for gender bias evaluation.

How to interpret the results returned by analyze():

- coefficient: raw effect size from the logistic regression model.
- odds_ratio: multiplicative change in the odds of a correct prediction.
    > 1.0: higher predictor value increases the odds of a correct prediction.
    < 1.0: higher predictor value decreases the odds of a correct prediction.
    = 1.0: no relationship.
- p_value: statistical significance (probability of observing this result by chance).
    < 0.05: statistically significant relationship.
    >= 0.05: not statistically significant.
- ci_lower / ci_upper: 95% confidence interval for odds_ratio.

Example: "Spanish: odds_ratio=0.57, p_value=0.38" -> higher stereotypicality is
associated with 43% lower odds of a correct prediction, but this is not
statistically significant (p > 0.05).
Example: "Spanish: odds_ratio=1.43, p_value=0.02" -> higher stereotypicality is
associated with 43% higher odds of a correct prediction, and this IS
statistically significant (p < 0.05).
"""

import pandas as pd
from typing import Dict, List, Any
import numpy as np
import statsmodels.api as sm
from ..dataset import DEvalDataset


class LogisticRegressionAnalysis:
    """Perform logistic regression to analyze relationships between predictors and prediction accuracy."""

    def __init__(self, ds: DEvalDataset, gold_col: str):
        self.ds = ds
        self.gold_col = gold_col

    def __prepare_data(self, language: str, predictor_col: str,df:pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """Prepare data for logistic regression analysis."""
        pred_col = self.ds.prediction_columns.get(language)

        if pred_col is None:
            raise ValueError(f"No prediction column found for language: {language}")

        if predictor_col not in df.columns:
            raise ValueError(f"Predictor column '{predictor_col}' not found in dataset")

        # Create accuracy outcome variable (1 = correct, 0 = incorrect)
        accuracy = (df[self.gold_col] == df[pred_col]).astype(int)
        predictor = df[predictor_col]

        analysis_df = pd.DataFrame({
            'accuracy': accuracy,
            'predictor': predictor
        })
        # Remove rows with missing values
        analysis_df = analysis_df.dropna()

        if len(analysis_df) == 0:
            raise ValueError("No valid data remaining after removing missing values")

        X = analysis_df[['predictor']]
        y = analysis_df['accuracy']

        return X, y

    def __fit_logistic_regression(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """Fit logistic regression model and return comprehensive results."""
        # Check for data quality issues
        if X['predictor'].nunique() <= 1:
            raise ValueError(f'Predictor variable has no variation (all values = {X["predictor"].iloc[0]})')

        if y.nunique() <= 1:
            raise ValueError(f'Outcome variable has no variation (all values = {y.iloc[0]})')

        # Standardize predictor for better interpretation (simple implementation)
        predictor_series = X['predictor']
        predictor_mean = float(predictor_series.mean())
        predictor_std = float(predictor_series.std())
        X_scaled = ((predictor_series - predictor_mean) / predictor_std).to_numpy().reshape(-1, 1)

        # Fit statsmodels model
        X_sm = sm.add_constant(X_scaled)
        sm_model = sm.Logit(y, X_sm).fit(disp=False)

        # Extract coefficients and statistics
        coef = sm_model.params.iloc[1]  # coefficient for predictor
        std_err = sm_model.bse.iloc[1]  # standard error
        p_value = sm_model.pvalues.iloc[1]  # p-value
        odds_ratio = np.exp(coef)  # odds ratio

        # Confidence intervals
        conf_int = sm_model.conf_int()
        ci_lower = np.exp(conf_int.iloc[1, 0])  # lower bound
        ci_upper = np.exp(conf_int.iloc[1, 1])  # upper bound

        return {
            'coefficient': coef,
            'std_error': std_err,
            'p_value': p_value,
            'odds_ratio': odds_ratio,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'n_observations': len(y),
        }

    def analyze(self, predictor_col: str, languages: List[str] | None = None,filter_col:str|None=None,filter_value:Any=None) -> pd.DataFrame:
        """Analyze predictor-accuracy relationships for multiple languages and return as DataFrame."""
        df=self.ds.df
        if filter_col is not None:
            df=df[df[filter_col]==filter_value]
        if languages is None:
            languages = list(self.ds.translation_columns.keys())

        if any(lang not in self.ds.translation_columns for lang in languages):
            raise ValueError(f"Some languages are not available in the dataset (unknown languages: {[lang for lang in languages if lang not in self.ds.translation_columns]})")

        if predictor_col not in df.columns:
            raise ValueError(f"Predictor column '{predictor_col}' not found in dataset")

        results_data = []

        for lang in languages:
            X, y = self.__prepare_data(lang, predictor_col,df)
            result = self.__fit_logistic_regression(X, y)
            row_data: Dict[str, Any] = {
                'language': lang,
                'coefficient': result['coefficient'],
                'odds_ratio': result['odds_ratio'],
                'p_value': result['p_value'],
                'ci_lower': result['ci_lower'],
                'ci_upper': result['ci_upper'],
                'n_observations': result['n_observations']
            }
            if filter_col is not None:
                row_data[filter_col] = filter_value
            results_data.append(row_data)

        return pd.DataFrame(results_data)
