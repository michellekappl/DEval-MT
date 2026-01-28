from declensions import (
    Adjective,
    DefinitePhrase,
    Name,
    Noun,
    Possessive,
    Pronoun,
    Relative,
)
# define constants for sentence styles
NORMAL_SENTENCE = 1
NORMAL_SENTENCE_PRONOUN = 2
ADJECTIVE_SENTENCE = 3
ADJECTIVE_SENTENCE_PRONOUN = 4
ROMANTIC_SENTENCE = 5
NAME_SENTENCE = 6

class Instance:
    """
    Represents a single instance of a template sentence.
    Provides string representation in a specific format for CSV output.
    """

    x: Noun
    """The first noun in the sentence."""
    sentence_style: str | int 
    """The style of the sentence"""
    sentence_id: int | None
    """The id of the sentence"""
    x_group: str | int
    """The group of the first noun (either "romantic" or a number corresponding to some job group)."""
    x_idx: int
    """The index of the first noun in the sentence (where "," is counted as a separate token)."""
    y: Noun | None
    """The second noun in the sentence, or None if this is a name sentence."""
    y_group: str | int | None
    """The group of the second noun (either "romantic" or a number corresponding to some job group), or None if this is a name (style 4) sentence."""
    y_idx: int | None
    """The index of the second noun in the sentence (where "," is counted as a separate token), or None if this is a name sentence."""
    adjective: Adjective | None
    """The adjective in the sentence (only for style 2 sentences)."""
    modified: str | None
    """Which noun was modified by the adjective, either "x" or "y" (only for style 2 sentences, None otherwise)."""
    text: str
    """The full text of the sentence with the nouns and adjectives replaced by their declensions."""
    name: Name | None
    """The name in the sentence (only for style 4 sentences, None otherwise)."""
    statistics: dict
    """The statistics for the job groups, used to calculate stereotypicality of the nouns."""

    def __init__(
        self,
        x: Noun,
        sentence_style: str | int,
        sentence_id: int | None,
        x_group: str | int,
        x_idx: int,
        y: Noun | None,
        y_group: str | int | None,
        y_idx: int | None,
        adjective: Adjective | None,
        modified: str | None,
        text: str,
        name: Name | None,
        statistics: dict,
    ):
        self.x = x
        self.sentence_style = sentence_style
        self.sentence_id = sentence_id
        self.y = y
        self.x_group = x_group
        self.y_group = y_group
        self.text = text
        self.adjective = adjective
        self.modified = modified  # "x" or "y", which one was modified
        self.x_idx = x_idx  # index of x in the sentence
        self.y_idx = y_idx  # index of y in the sentence
        self.name = name
        self.statistics = statistics
        # id adjectives shift sentence_style to adjective 
        if(adjective):
            self.sentence_style += 2

    header = (
        "sentence_style;"
        "sentence_id;"
        "x_nom_sg;x_group;x_gender;x_idx;x_stereotypical;x_level;"
        "y_nom_sg;y_group;y_gender;y_idx;y_stereotypical;y_level;"
        "adjective;modified;name;name_gender;text"
    )
    """The header for the CSV file, describing the fields in the same order as they are in the string representation."""

    def __str__(self):
        return (
            f"{self.sentence_style};"
            + f"{self.sentence_id};"
            + f"{self.x.nom_sg};{self.x_group};{self.x.gender};{self.x_idx};{self.x_stereotypical};{self.x.status or 'none'};"
            + (
                f"{self.y.nom_sg};{self.y_group};{self.y.gender};{self.y_idx};{self.y_stereotypical};{self.y.status or 'none'};"
                if self.y
                else "none;none;none;none;none;none;"
            )
            + f"{self.adjective.text if self.adjective else 'none'};"
            + f"{self.modified or 'none'};"
            + (f"{self.name.text};{self.name.gender};" if self.name else "none;none;")
            + f"{self.text}"
        )

    @property
    def x_stereotypical(self) -> float:
        """The stereotypicality of the first noun: if x has gender g (m or f), then this is `num_g / (num_m + num_f)`,
        where `num_m` and `num_f` are the number of male and female instances, respectively.
        NaN if unapplicable."""
        if (
            self.sentence_style == NAME_SENTENCE
            or self.sentence_style == ROMANTIC_SENTENCE
        ):
            return float("nan")
        else:
            num_m, num_f = self.statistics[self.x_group][self.x.status]
            if num_m == 0 and num_f == 0:
                return float("nan")
            if self.x.gender == "m":
                return num_m / (num_m + num_f)
            elif self.x.gender == "f":
                return num_f / (num_m + num_f)
            else:
                return float("nan")

    @property
    def y_stereotypical(self) -> float:
        """The stereotypicality of the second noun: if y has gender g (m or f), then this is `num_g / (num_m + num_f)`,
        where `num_m` and `num_f` are the number of male and female instances, respectively.
        NaN if unapplicable."""
        if not self.y or self.sentence_style == ROMANTIC_SENTENCE:
            return float("nan")
        else:
            num_m, num_f = self.statistics[self.y_group][self.y.status]

            if num_m == 0 and num_f == 0:
                return float("nan")
            if self.y.gender == "m":
                return num_m / (num_m + num_f)
            elif self.y.gender == "f":
                return num_f / (num_m + num_f)
            else:
                return float("nan")
