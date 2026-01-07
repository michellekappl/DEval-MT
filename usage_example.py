"""Example usage of the modular analysis system for DEval-MT."""

import os
import pandas as pd
import numpy as np
from Dataset import DEvalDataset
from analysis import (
   ErrorAnalysis,
   ConfusionMatrix,
   LogisticRegressionAnalysis,
)
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.hebrew_morph_analyzer import HebrewMorphAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer
from sdk import run_subject_pipeline

def example_data() -> DEvalDataset:
   # if style_processed file aready exists, load it
   if os.path.exists(f"test_data_processed.csv"):
      ds = DEvalDataset.from_csv(f"test_data_processed.csv", text_column="text", sep=";", translation_columns={
         "es": "es",
         "fr": "fr",
         "ar": "ar",
         "he": "he"
      }, prediction_columns={
         "es": "x_gender_es",
         "fr": "x_gender_fr",
         "ar": "x_gender_ar",
         "he": "x_gender_he"
      })
      return ds
   else:
      print(f"test_data_processed.csv not found, creating from scratch...")
      df = pd.read_csv(f"test_data/test_data.csv", sep=";")
      ds = DEvalDataset(df, text_column="text")

      # load translations from a file
      list_of_es_translations = pd.read_csv(f"test_data/translations/es.txt", header=None, sep=";")[0].tolist()
      list_of_fr_translations = pd.read_csv(f"test_data/translations/fr.txt", header=None, sep=";")[0].tolist()
      list_of_ar_translations = pd.read_csv(f"test_data/translations/ar.txt", header=None, sep=";")[0].tolist()
      list_of_he_translations = pd.read_csv(f"test_data/translations/he.txt", header=None, sep=";")[0].tolist()

      # Add translations (must match row count)
      ds.add_translations("es", list_of_es_translations, "es")
      ds.add_translations("fr", list_of_fr_translations, "fr")
      ds.add_translations("ar", list_of_ar_translations, "ar")
      ds.add_translations("he", list_of_he_translations, "he")

      # Build and load analyzers explicitly
      morph_es = SpaCyMorphAnalyzer("es_dep_news_trf"); morph_es.load()
      morph_fr = SpaCyMorphAnalyzer("fr_dep_news_trf"); morph_fr.load()
      morph_ar = QalsadiMorphAnalyzer()
      morph_he = HebrewMorphAnalyzer()

      analyzers: dict[str, BaseMorphologicalAnalyzer] = {
         "es": morph_es,
         "fr": morph_fr,
         "ar": morph_ar,
         "he": morph_he,
      }

      # Run for x subject
      df_x = run_subject_pipeline(
         ds,
         analyzers=analyzers,
         source_column="text",
         subject_index_column="x_idx",
         output_prefix="x",
         article_offset=-1,
         use_multiprocessing=False
      )

      return ds
   
"""Run comprehensive examples of all analysis methods."""
print("=== DEval-MT Analysis Examples ===\n")

# Create sample data
if __name__ == '__main__':
   ds1 = example_data()
   ds1.df.to_csv("test_data_processed.csv", sep=";", index=False)

# 1. Error Analysis
print("1. ERROR ANALYSIS")
print("-" * 50)
error_analyzer = ErrorAnalysis(ds1, 'x_gender')
print(error_analyzer.analyze().T)


# 2. Confusion Matrix
print("2. CONFUSION MATRIX")
print("-" * 50)
cm_analyzer = ConfusionMatrix(ds1, 'x_gender')
print(cm_analyzer.analyze().T)

# 3. Logistic Regression Analysis
print("3. LOGISTIC REGRESSION ANALYSIS")
print("-" * 50)
lr_analyzer = LogisticRegressionAnalysis(ds1, 'x_gender')
lr_results = lr_analyzer.analyze(predictor_col='x_stereotypical')
print("Logistic Regression Results:")
print(lr_results.to_string(index=False))

"""
HOW TO INTERPRET LOGISTIC REGRESSION RESULTS:

• coefficient: Raw effect size from logistic regression model
• odds_ratio: Multiplicative change in odds of correct prediction
   - > 1.0: Higher stereotypicality increases correct prediction odds
   - < 1.0: Higher stereotypicality decreases correct prediction odds
   - = 1.0: No relationship
• p_value: Statistical significance (probability of observing this result by chance)
   - < 0.05: Statistically significant relationship
   - ≥ 0.05: Not statistically significant
• ci_lower/upper: 95% confidence interval for odds_ratio

EXAMPLE INTERPRETATION:
"Spanish: odds_ratio=0.57, p_value=0.38"
→ Higher stereotypicality is associated with 43% lower odds of correct prediction
→ But this relationship is not statistically significant (p > 0.05)

"Spanish: odds_ratio=1.43, p_value=0.02"
→ Higher stereotypicality is associated with 43% higher odds of correct prediction
→ This relationship IS statistically significant (p < 0.05)

"""