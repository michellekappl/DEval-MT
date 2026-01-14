from typing import List

from morphological_analysis.gender import Gender
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken
from spacy.lang.he import Hebrew


class HebrewMorphAnalyzer(BaseMorphologicalAnalyzer):
    def __init__(self):
        self.tokenizer = Hebrew().tokenizer

    def tokenize_sentence(self, text: str) -> List[MorphologicalToken]:
        doc = self.tokenizer(text)
        tokens = []

        for token in doc:
            gender = (
                Gender.FEMININE if token.text[-1] in ["ת", "ה"]
                else Gender.MASCULINE
            )
            tokens.append(MorphologicalToken(
                text=token.text,
                gender=gender,
                pos=token.pos_,
            ))

        return tokens

    def get_phrase_gender(self, tokens: List[MorphologicalToken]) -> Gender:
        for token in tokens:
            if token.gender == Gender.FEMININE:
                return Gender.FEMININE
        return Gender.MASCULINE
