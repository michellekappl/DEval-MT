"""Public API for morphological analysis.

Exported symbols (stable):
 - BaseMorphologicalAnalyzer (abstract base type)
 - MorphologicalToken (data container)
 - Gender (enum for grammatical gender)
 - SpaCyAnalyzer (spaCy-based implementation)
 - SemiticAnalyzer (qalsadi / Semitic languages implementation)

Factory / manager utilities are intentionally NOT exported here to keep the
surface minimal; import them from their modules directly if needed and treat
as internal APIs.
"""

from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer, MorphologicalToken
from morphological_analysis.gender import Gender
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.qalsadi_morph_analyzer import QalsadiMorphAnalyzer

__all__ = [
   'BaseMorphologicalAnalyzer',
   'MorphologicalToken',
   'Gender',
   'SpaCyMorphAnalyzer',
   'QalsadiMorphAnalyzer',
]
