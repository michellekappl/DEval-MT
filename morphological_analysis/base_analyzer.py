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

        # Include all genders including UNKNOWN for counting
        genders = [token.gender for token in tokens if token.gender is not None]
        if not genders:
            return Gender.UNKNOWN

        # Count occurrences of each gender among the provided tokens
        counts = Counter(genders)
        most_common = counts.most_common()
        if len(most_common) == 0:
            return Gender.UNKNOWN

        # If UNKNOWN is the most common, use the second most common instead
        if most_common[0][0] == Gender.UNKNOWN:
            if len(most_common) > 1:
                # Check for tie between second and third
                if len(most_common) > 2 and most_common[1][1] == most_common[2][1]:
                    return Gender.UNKNOWN  # It's a draw between non-UNKNOWN genders
                return most_common[1][0] or Gender.UNKNOWN
            else:
                return Gender.UNKNOWN

        # Check for ties (excluding UNKNOWN from tie consideration)
        if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
            # If tied with UNKNOWN, use the non-UNKNOWN one
            if most_common[1][0] == Gender.UNKNOWN:
                return most_common[0][0] or Gender.UNKNOWN
            return Gender.UNKNOWN  # It's a draw between two non-UNKNOWN genders

        return most_common[0][0] or Gender.UNKNOWN
