import spacy
from typing import List

from morphological_analysis.gender import Gender
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken

class SpaCyMorphAnalyzer(BaseMorphologicalAnalyzer):
    """Morphological analyzer using spaCy models. Can be used for multiple languages, depending on the loaded model."""
    def __init__(self, spacy_model: str) -> None:
        self.spacy_model = spacy_model
        self._loaded = False
        self.nlp = None

    def load(self) -> None:
        self.nlp = spacy.load(self.spacy_model)
        self._loaded = True

    def tokenize_sentence(self, text: str) -> List[MorphologicalToken]:
        if not self._loaded or self.nlp is None:
            raise RuntimeError("Analyzer not loaded. Call load() first.")
        
        doc = self.nlp(text)
        tokens = []
        
        for token in doc:
            spacy_gender = token.morph.get("Gender", default=["Unknown"])[0] # Index element 0, because morph.get always returns a list, which will only ever have one element for gender
            gender = (
                Gender.FEMININE if spacy_gender == "Fem"
                else Gender.MASCULINE if spacy_gender == "Masc"
                else Gender.NEUTER if spacy_gender == "Neut" 
                else Gender.UNKNOWN
            )
            tokens.append(MorphologicalToken(
                text=token.text,
                gender=gender,
                pos=token.pos_,
            ))
        return tokens