from abc import ABC, abstractmethod
from collections import Counter
from typing import List, Optional

from morphological_analysis.gender import Gender

class MorphologicalToken:
    """Standardized token representation to be used by all analyzers."""
    def __init__(self, text: str, gender: Optional[Gender] = None, pos: Optional[str] = None):
        self.text = text
        self.gender = gender
        self.pos = pos

class BaseMorphologicalAnalyzer(ABC):
    """Abstract base class for all morphological analyzers"""
    
    @abstractmethod
    def tokenize_sentence(self, text: str) -> List[MorphologicalToken]:
        """
        Analyzes the input text and returns a list of MorphologicalToken objects, each representing a token with associated morphological information.
        Args:
            text (str): The input text to be tokenized and analyzed.
        Returns:
            List[MorphologicalToken]: A list of tokens with morphological analysis results.
        """
        pass
    
    def get_phrase_gender(self, tokens: List[MorphologicalToken]) -> Gender:
        """
        Determines the predominant gender of a phrase.
        Args:
            phrase (str): The input phrase whose gender is to be determined.
        Returns:
            Gender: The predicted gender of the phrase.
        """
        if not tokens:
            return Gender.UNKNOWN

        genders = [token.gender for token in tokens if token.gender != Gender.UNKNOWN]
        if not genders:
            return Gender.UNKNOWN

        # Count occurrences of each gender among the provided tokens and return the most common one.
        # Ties result in UNKNOWN.
        # This is a simple heuristic and a good starting point for improvement :)
        counts = Counter(genders)
        most_common = counts.most_common()
        if len(most_common) == 0:
            return Gender.UNKNOWN
        if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
            return Gender.UNKNOWN  # It's a draw
        return most_common[0][0] or Gender.UNKNOWN
