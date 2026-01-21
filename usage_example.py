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
   # if style_processed file already exists, load it
   if os.path.exists(f"gpt-4o_processed.csv"):
      ds = DEvalDataset.from_csv(f"gpt-4o_processed.csv", text_column="text", sep=";", translation_columns={
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
      print(f"processed file not found, creating from scratch...")
      path_to_ds='DEval_dataset.csv'
      df = pd.read_csv(path_to_ds, sep=";")
      ds = DEvalDataset(df, text_column="text")

      # load translations from a file
      list_of_es_translations = pd.read_csv(f"test_data/test_translations/es_gpt-4o.txt", header=None, sep=";")[0].tolist()
      list_of_fr_translations = pd.read_csv(f"test_data/test_translations/fr_gpt-4o.txt", header=None, sep=";")[0].tolist()
      list_of_ar_translations = pd.read_csv(f"test_data/test_translations/ar_gpt-4o.txt", header=None, sep=";")[0].tolist()
      list_of_he_translations = pd.read_csv(f"test_data/test_translations/he_gpt-4o.txt", header=None, sep=";")[0].tolist()

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
   ds1.df.to_csv("gpt-4o_processed.csv", sep=";", index=False)

# 1. Error Analysis
print("1. ERROR ANALYSIS")
print("-" * 50)
error_analyzer = ErrorAnalysis(ds1, 'x_gender')
# example: for sentence_style==1:
# print(error_analyzer.analyze(filter_col='sentence_style',filter_value=1).T)
# example: checking all sentence_styles:
for style in ds1.df['sentence_style'].unique():
   print('---')
   print(ErrorAnalysis(ds1, "x_gender").analyze(filter_col='sentence_style',filter_value=style).T)

# print(error_analyzer.analyze().T)


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

'''
Example for error analysis with filter column==sentence_style:
1. ERROR ANALYSIS
--------------------------------------------------
                       0         1         2         3
language              es        fr        ar        he
sentence_style         2         2         2         2
total               1118      1118      1118      1118
correct             1009       991       692       936
accuracy        0.902504  0.886404  0.618962  0.837209
error_count          109       127       426       182
---
                       0         1         2         3
language              es        fr        ar        he
sentence_style         4         4         4         4
total               1060      1060      1060      1060
correct              558       708       873       943
accuracy        0.526415  0.667925  0.823585  0.889623
error_count          502       352       187       117
---
                       0         1         2         3
language              es        fr        ar        he
sentence_style         1         1         1         1
total               1118      1118      1118      1118
correct             1005       989       707       911
accuracy        0.898927  0.884615  0.632379  0.814848
error_count          113       129       411       207
---
                       0         1         2         3
language              es        fr        ar        he
sentence_style         3         3         3         3
total               1060      1060      1060      1060
correct              555       707       864       925
accuracy        0.523585  0.666981  0.815094  0.872642
error_count          505       353       196       135
'''