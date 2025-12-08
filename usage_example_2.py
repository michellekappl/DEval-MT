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
from sdk import run_subject_pipeline

# Import plotting functions from your modular package
from plots import (
   plot_error_analysis,
   plot_confusion_matrix,
   plot_logistic_regression,
   save_dataframes
)

def example_data() -> DEvalDataset:
   if os.path.exists("test_data_processed.csv"):
      ds = DEvalDataset.from_csv("test_data_processed.csv", text_column="text", sep=";", translation_columns={
         "es": "es",
         "fr": "fr"
      }, prediction_columns={
         "es": "x_gender_es",
         "fr": "x_gender_fr"
      })
      return ds
   else:
      print("test_data_processed.csv not found, creating from scratch...")
      df = pd.read_csv("test_data/test_data.csv", sep=";")
      ds = DEvalDataset(df, text_column="text")

      list_of_es_translations = pd.read_csv("test_data/translations/es.txt", header=None, sep=";")[0].tolist()
      list_of_fr_translations = pd.read_csv("test_data/translations/fr.txt", header=None, sep=";")[0].tolist()

      ds.add_translations("es", list_of_es_translations, "es")
      ds.add_translations("fr", list_of_fr_translations, "fr")

      morph_es = SpaCyMorphAnalyzer("es_dep_news_trf"); morph_es.load()
      morph_fr = SpaCyMorphAnalyzer("fr_dep_news_trf"); morph_fr.load()
      analyzers: dict[str, BaseMorphologicalAnalyzer] = {
         "es": morph_es,
         "fr": morph_fr,
      }

      run_subject_pipeline(
         ds,
         analyzers=analyzers,
         source_column="text",
         subject_index_column="x_idx",
         output_prefix="x",
         article_offset=-1,
         use_multiprocessing=False
      )

      return ds

if __name__ == '__main__':
   ds1 = example_data()
   ds1.df.to_csv("test_data_processed.csv", sep=";", index=False)

   # 1. Error Analysis
   print("1. ERROR ANALYSIS")
   print("-" * 50)
   error_analyzer = ErrorAnalysis(ds1, 'x_gender')
   error_df = error_analyzer.analyze().T
   print(error_df)

   # 2. Confusion Matrix
   print("2. CONFUSION MATRIX")
   print("-" * 50)
   cm_analyzer = ConfusionMatrix(ds1, 'x_gender')
   cm_df = cm_analyzer.analyze().T
   print(cm_df)
   
   # 3. Logistic Regression Analysis
   print("3. LOGISTIC REGRESSION ANALYSIS")
   print("-" * 50)
   lr_analyzer = LogisticRegressionAnalysis(ds1, 'x_gender')
   lr_results = lr_analyzer.analyze(predictor_col='x_stereotypical')
   print("Logistic Regression Results:")
   print(lr_results.to_string(index=False))

   #label the file names on the dataframes, otherwise it will use df_1, df_2 etc.   
   cm_df.attrs["filename"] = "confusion_matrix"
   error_df.attrs["filename"] = "error_analysis"
   lr_results.attrs["filename"] = "logistic_regression"

   save_dataframes(error_df, cm_df, lr_results)
   
   plot_error_analysis(error_df.T)
   plot_confusion_matrix(cm_df.T)
   plot_logistic_regression(lr_results)
