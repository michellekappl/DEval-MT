from typing import List

from morphological_analysis.gender import Gender
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken
import qalsadi.analex as qa
from collections import Counter

class QalsadiMorphAnalyzer(BaseMorphologicalAnalyzer):
   """Morphological analyzer using the Qalsadi library for Arabic."""
   def __init__(self):
      self.qa = qa.Analex()

   def tokenize_sentence(self, text: str) -> List[MorphologicalToken]:
      # Get morphological interpretations for each word in the text
      # Each token has multiple possible interpretations that are returned by qalsadi.
      interpretations = self.qa.check_text(text)
      tokens = [
         MorphologicalToken(
            text=word[0]["word"],  # Extract the word text from the first interpretation
            # Determine the most common gender tag among all interpretations for this word
            gender=[Gender.UNKNOWN, Gender.MASCULINE, Gender.UNKNOWN, Gender.FEMININE][Counter([interp["tag_gender"] for interp in word]).most_common(1)[0][0]]
            if word else Gender.UNKNOWN  # If no interpretations, set gender as UNKNOWN
         )
         for word in interpretations  # Iterate over each word's interpretations
      ]
      return tokens
   
   def get_phrase_gender(self, tokens: List[MorphologicalToken]) -> Gender:
      if not tokens:
            return Gender.UNKNOWN

      genders = [token.gender for token in tokens if token.gender != Gender.UNKNOWN]
      if not genders:
         return Gender.UNKNOWN

      counts = Counter(genders)
      most_common = counts.most_common()
      if len(most_common) == 0:
         return Gender.UNKNOWN
      if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
         return Gender.UNKNOWN  # It's a draw
      return most_common[0][0] or Gender.UNKNOWN
   