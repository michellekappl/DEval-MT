"""Error Analysis for gender bias evaluation in MT outputs."""

from enum import Enum
import pandas as pd
from typing import List
from Dataset import DEvalDataset
from morphological_analysis.gender import Gender

class ErrorType(Enum):
      M_TO_F = "m→f"
      M_TO_N = "m→n"
      M_TO_U = "m→u"
      M_TO_D = "m→d"

      F_TO_M = "f→m"
      F_TO_N = "f→n"
      F_TO_U = "f→u"
      F_TO_D = "f→d"

      N_TO_M = "n→m"
      N_TO_F = "n→f"
      N_TO_U = "n→u"
      N_TO_D = "n→d"

      U_TO_M = "u→m"
      U_TO_F = "u→f"
      U_TO_N = "u→n"
      U_TO_D = "u→d"

      D_TO_M = "d→m"
      D_TO_F = "d→f"
      D_TO_N = "d→n"
      D_TO_U = "d→u"

      @classmethod
      def from_genders(cls, gold: Gender, pred: Gender) -> 'ErrorType':
         """Create ErrorType from gold and predicted gender values."""
         gender_map = {
            Gender.MASCULINE: 'M',
            Gender.FEMININE: 'F',
            Gender.NEUTER: 'N',
            Gender.UNKNOWN: 'U',
            Gender.DIVERSE: 'D'
         }

         gold_char = gender_map.get(gold, 'U')
         pred_char = gender_map.get(pred, 'U')

         error_name = f"{gold_char}_TO_{pred_char}"

         return cls[error_name]

class ErrorAnalysis: 
   def __init__(self, ds: DEvalDataset, gold_col: str):
      self.ds = ds
      self.gold_col = gold_col

   def analyze(self, languages: List[str] | None = None, *, analyze_error_patterns: bool = True,filter_col:str|None=None,filter_value=None) -> pd.DataFrame:
      df=self.ds.df
      if filter_col is not None:
         df=df[df[filter_col]==filter_value]
      
      if languages is None:
         languages = list(self.ds.translation_columns.keys())

      if any(lang not in self.ds.translation_columns for lang in languages):
         raise ValueError(f"Some languages are not available in the dataset (unknown languages: {[lang for lang in languages if lang not in self.ds.translation_columns]})")

      results_data = []

      for lang in languages:
         pred_col = self.ds.prediction_columns.get(lang)
         total = len(df) #len(self.ds.df)
         prediction_correct = df[df[self.gold_col] == df[pred_col]]
         
         correct = len(prediction_correct)
         accuracy = correct / total if total > 0 else 0.0

         # error_types = {
         #    ErrorType.M_TO_F: 0,
         #    ErrorType.M_TO_N: 0,
         #    ErrorType.M_TO_U: 0,
         #    ErrorType.M_TO_D: 0,
         #    ErrorType.F_TO_M: 0,
         #    ErrorType.F_TO_N: 0,
         #    ErrorType.F_TO_U: 0,
         #    ErrorType.F_TO_D: 0,
         #    ErrorType.N_TO_M: 0,
         #    ErrorType.N_TO_F: 0,
         #    ErrorType.N_TO_U: 0,
         #    ErrorType.N_TO_D: 0,
         #    ErrorType.U_TO_M: 0,
         #    ErrorType.U_TO_F: 0,
         #    ErrorType.U_TO_N: 0,
         #    ErrorType.U_TO_D: 0,
         #    ErrorType.D_TO_M: 0,
         #    ErrorType.D_TO_F: 0,
         #    ErrorType.D_TO_N: 0,
         #    ErrorType.D_TO_U: 0,
         # }
         error_types={et:0 for et in ErrorType}

         for _, row in df.iterrows():
            gold = row.get(self.gold_col)
            pred = row.get(pred_col)

            if gold == Gender.UNKNOWN or pred == Gender.UNKNOWN:
               continue

            if gold is not None and pred is not None and gold != pred:
               error_types[ErrorType.from_genders(Gender[gold], Gender[pred])] += 1

         # Create a row for this language
         row_data = {
            'language': lang,
            f'{filter_col}':filter_value,
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'error_count': total - correct
         }

         # Add error type counts
         # for error_type, count in error_types.items():
         #    row_data[f'error_{error_type.name.lower()}'] = count
         
         # if filter_col is not None:
         #    row_data[filter_col]=filter_value

         results_data.append(row_data)

      return pd.DataFrame(results_data)
