import random
import re
from itertools import chain
from typing import Literal, TypeVar

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


T = TypeVar("T")


def from_none(arg: T | None) -> T:
    """
    Only here for type checking and error reporting purposes. Returns an argument unchanged if it is not None.
    """
    if not arg:
        raise ValueError("Argument cannot be None")
    return arg


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


class Template:
    """
    Represents a template sentence with placeholders for nouns and adjectives.
    Provides methods to generate instances of the template with specific nouns and adjectives.
    """

    generic: bool = False
    """Whether this template is generic, i.e. it can be used for any job group."""

    sentence_style: Literal[1]

    def __init__(
        self,
        row: list[str],
        statistics: dict,
        groups: dict[str | int, list[list[Noun]]],
        adjectives: list[Adjective],
        names: list[Name],
    ):
        """
        Initializes the template with a sentence, hierarchy, and groups of nouns.

        Parameters
        ----------
        row : list[str]
            A list containing the sentence template, hierarchy, and groups of nouns.
        statistics : dict
            A dictionary containing statistics for the job groups, used to calculate stereotypicality of the nouns.
        groups : dict[str | int, list[list[Noun]]]
            A dictionary mapping group names or numbers to lists of nouns.
        adjectives : list[Adjective]
            A list of adjectives to use in the template.
        names : list[Name]
            A list of names to use in the template.
        """
        groups_list = [
            (x_group, x) for x_group, xs in groups.items() for job in xs for x in job
        ]

        self.sentence = row[0].strip()  # the actual sentence template
        self.sentence_id = row[2].strip()
        self.statistics = statistics
        self.adjectives = adjectives  # adjectives to use in template
        self.groups = groups  # groups to use in template
        self.names = names  # names to use in template

        # the hierarchy of the template, i.e. "x>y", "x<y" or "none"
        hierarchy = "none"

        self.higher = None  # the higher group in the hierarchy, either "x" or "y", or None if no hierarchy is defined

        # parse hierarchy
        if hierarchy != "none":
            if ">" in hierarchy or "<" in hierarchy:
                # check that the hierarchy variable is x or y
                if hierarchy[0] in (
                    "x",
                    "y",
                ):
                    self.higher = hierarchy[0]
                else:
                    raise ValueError(f"Invalid hierarchy: {hierarchy}")
            else:
                raise ValueError(f"Invalid hierarchy: {hierarchy}")

        # add all the relevant jobs to the xs list
        # the xs list is of the form [(group_id, Noun), ...]
        self.xs: list[tuple[str | int, Noun]] = []

        self.matching_x_groups: list[str | int] = []
        sentence_style = row[1].strip("<>") 

        if sentence_style == "normal_pron":
            self.sentence_style = NORMAL_SENTENCE_PRONOUN
        elif sentence_style == "romantic":
            self.sentence_style = ROMANTIC_SENTENCE
        elif sentence_style == "name":
            self.sentence_style = NAME_SENTENCE
        else:
            self.sentence_style = NORMAL_SENTENCE
        # parse x groups from the row (this is a string of the form '[111, "romantic", 333]')
        x_groups = [""]

        if x_groups[0] == "":
            self.generic = True
            self.xs = groups_list
        elif x_groups[0] == "romantic":
            self.sentence_style = ROMANTIC_SENTENCE
            self.xs = [
                (x_group, x) for x_group, x in groups_list if x_group == "romantic"
            ]
            self.matching_x_groups = ["romantic"]
        else:
            matching_groups = [
                int(group) if group != "romantic" else group for group in x_groups
            ]
            self.xs = [
                (x_group, x) for x_group, x in groups_list if x_group in matching_groups
            ]
            self.matching_x_groups = matching_groups

        # check if there is a <y> value in the sentence
        # if not, then this is a name (style 4) sentence
        # if "<y" not in self.sentence:
        #     self.sentence_style = NAME_SENTENCE

        # otherwise, do exactly the same for ys
        if self.sentence_style != NAME_SENTENCE:
            matching_y_groups = []
            self.ys = []
            self.ys_by_gender: list[
                tuple[
                    int | str,
                    list[Noun],
                ]
            ] = []
            y_groups = [""]
            if y_groups[0] == "":
                self.ys = groups_list
                matching_y_groups = list(groups.keys())
            elif y_groups[0] == "romantic":
                self.sentence_style = ROMANTIC_SENTENCE
                matching_y_groups = ["romantic"]
            else:
                matching_y_groups = [
                    int(group) if group != "romantic" else group for group in y_groups
                ]

            self.ys = [
                (y_group, y)
                for y_group, y in groups_list
                if y_group in matching_y_groups
            ]
            # necessary as we need to make sure that in the function gen_for_x,
            # we can always find an argument of another gender
            self.ys_by_gender = [
                (y_group, y_genders)
                for y_group, y_list in groups.items()
                for y_genders in y_list
                if y_group in matching_y_groups
            ]

    def resolve_name(
        self,
        x: Noun,
        name: Name,
        match: re.Match,
    ) -> str:
        """
        Resolve a replacement within a name sentence, i.e. given a selected noun x and a name for this sentence,
        return the correct word form of the matched expression (something like <name> or <x_nom_sg>).

        Parameters
        ----------
        x : Noun
            The selected noun for the sentence, which will be declined.
        name : Name
            The name to be used in the sentence, which will be declined.
        match: re.Match
            The match object containing the matched expression.
        """
        # split match by underscores
        parts = match.group(1).split("_")
        if parts[0] == "x" and parts[1] == "indef":
            # if the match is for x, decline it according to the case
            return x.decline(parts[2], "sg")
        elif parts[0] == "name":
            # we only have nominative case in our dataset for names
            return name.decline("nom", "sg")
        else:
            # throw error
            raise ValueError(f"Unknown match type: {parts[0]} in {match.group(1)}")

    def resolve(
        self,
        x: Noun,
        y: Noun,
        adjective: Adjective | None,
        modified: str | None,
        match: re.Match,
    ):
        """
        Resolve a replacement within a template sentence, i.e. given two selected nouns x and y
        and an optional adjective, return the correct word form of the matched expression
        (something like <x_nom_sg> or <y_gen_pl>).

        Parameters
        ----------
        x : Noun
            The first selected noun for the sentence.
        y : Noun
            The second selected noun for the sentence.
        adjective : Adjective | None
            The adjective to be used in the sentence.
        modified : str | None
            If there is an adjective: Which noun was modified by the adjective, either "x" or "y".
        match : re.Match
            The match object containing the matched expression.
        """
        # split match by underscores
        parts = match.group(1).split("_")

        # find the base noun
        base_noun = x if parts[0] == "x" else y

        if parts[1] in [
            "nom",
            "gen",
            "dat",
            "acc",
        ]:
            # case that this is a simply a definite noun phrase like <x_nom_sg>
            if adjective and parts[0] == modified:
                # if we have an adjective and the noun is the modified one, use it
                return DefinitePhrase(base_noun, adjective).decline(parts[1], "sg")
            else:
                return DefinitePhrase(base_noun).decline(parts[1], "sg")
        elif parts[1] == "rel":
            # case that this is a relative pronoun like <x_rel_nom>
            case = parts[2]
            return Relative(base_noun).decline(case, "sg")
        elif parts[1] == "pron":
            # case that this is a pronoun like <x_pron_nom>
            case = parts[2]
            return Pronoun(base_noun).decline(case, "sg")
        elif parts[1] == "poss":
            # case that this is a possessive pronoun like <x_poss_f_nom> or <x_poss_nom>
            if len(parts) == 4:
                # this is the case where we know the gender of the possessed noun (i.e. it doesn't change)
                # so something like <x_poss_f_nom>
                gender = parts[2]
                case = parts[3]
                return Possessive(base_noun, gender).decline(case, "sg")
            elif len(parts) == 3:
                # case where gender is not known, so we need to use the other noun to determine it
                # something like <x_poss_acc>
                other_noun = y if parts[0] == "x" else x  # complement to base_noun
                case = parts[2]
                return Possessive(
                    base_noun,
                    other_noun.grammatical_gender,
                ).decline(case, "sg")
            elif(len(parts) > 0):
                # case where gender is not known, so we need to use the other noun to determine it
                # something like <x_poss_acc>
                other_noun = y if parts[0] == "x" else x  # complement to base_noun
                case = parts[4]
                return Possessive(
                    base_noun,
                    other_noun.grammatical_gender,
                ).decline(case, "sg")
        elif parts[1] == "indef":
            # case that this is an indefinite noun phrase like <x_indef_nom>
            case = parts[2]
            return base_noun.decline(case, "sg")
        else:
            # throw error
            raise ValueError(f"Unknown match type: {parts}")

    def satisfies_hierarchy(self, x: Noun, y: Noun) -> bool:
        """
        Checks whether the two selected nouns satisfy the hierarchy defined in the template.
        If the hierarchy is `None`, returns `True`.
        """
        if self.higher is None:
            return True
        elif not hasattr(x, "status") or not hasattr(y, "status"):
            # if x or y do not have a status, we cannot compare them
            return False

        STATUS_HIERARCHY = {
            "Experten": 4,
            "Spezialisten": 3,
            "Fachkraefte": 2,
            "Helfer": 1,
        }

        if self.higher == "x":
            return (
                STATUS_HIERARCHY[from_none(x.status)]
                > STATUS_HIERARCHY[from_none(y.status)]
            )
        elif self.higher == "y":
            return (
                STATUS_HIERARCHY[from_none(x.status)]
                < STATUS_HIERARCHY[from_none(y.status)]
            )
        else:
            raise ValueError(f"Invalid hierarchy: {self.higher}")

    @staticmethod
    def find_indices(
        text: str,
        x: Noun,
        y: Noun | None,
    ) -> tuple[int | None, int | None]:
        """
        Finds the indices of the first occurrences of x and y in the text.
        If y is None, returns None for the second index.
        """
        x_idx, y_idx = None, None
        for idx, word in enumerate(text.replace(",", " ,").replace(".", " .").split()):
            if word in [
                x.nom_sg,
                x.gen_sg,
                x.dat_sg,
                x.acc_sg,
                # plurals are unused so far, so we can skip this
                x.nom_pl,
                x.gen_pl,
                x.dat_pl,
                x.acc_pl,
            ]:
                x_idx = idx
            elif y and word in [
                y.nom_sg,
                y.gen_sg,
                y.dat_sg,
                y.acc_sg,
                # y.nom_pl,
                # y.gen_pl,
                # y.dat_pl,
                # y.acc_pl,
            ]:
                y_idx = idx

        return x_idx, y_idx

    def gen_name(
        self,
        xs: list[tuple[str | int, Noun]] = [],
        matching_names: list[Name] = [],
    ) -> list[Name]:
        """
        Generates instances of the template sentence by replacing placeholders with actual names.
        This method generates instances for the name sentence style (4), where only names are used.
        Parameters
        ----------
        xs : list[tuple[str, Noun]], optional
            A list of tuples containing the group name and the noun for the first placeholder (x).
            If empty, the default nouns from the template will be used.
        matching_names : list[Name], optional
            A list of names to use in the generated instances. If empty, all names will be used.
        """
        if not matching_names:
            matching_names = self.names
        if self.sentence_style != NAME_SENTENCE:
            raise ValueError("This method can only be used for name sentences.")

        # if xs is empty, use the default ones
        if not xs:
            xs = self.xs

        instances = []
        # if this is a name sentence, we only need to generate instances with names
        for x_group, x, name in (
            (x_group, x, name)
            for x_group, x in xs
            for name in matching_names
            if name.gender == x.gender or name.gender == "n"
        ):
            # use regex to perform substitutions
            text = re.sub(
                r"<([a-zA-Z_]*)>",
                lambda m: self.resolve_name(x, name, m),
                self.sentence,
            )
            # capitalize the first letter of the substitution
            text = text[0].upper() + text[1:]
            # find index for x
            x_idx, _ = self.find_indices(text, x, None)
            # create instance with the determined paramters
            instance = Instance(
                x,
                self.sentence_style,
                None,
                x_group,
                from_none(x_idx),
                None,
                None,
                None,
                None,
                None,
                text,
                name,
                self.statistics,
            )
            # add to list of all instances
            instances.append(instance)

        return instances

    def gen_romantic(
        self,
        xs: list[tuple[str | int, Noun]] = [],
        ys: list[tuple[str | int, Noun]] = [],
    ):
        """
        Generates instances of the template sentence by replacing placeholders with actual nouns.
        This method generates instances for the romantic sentence style (3), where either x or y is in the romantic group.
        Parameters
        ----------
        xs : list[tuple[str | int, Noun]], optional
            A list of tuples containing the group name and the noun for the first placeholder (x).
            If empty, the default nouns from the template will be used.
        ys : list[tuple[str | int, Noun]], optional
            A list of tuples containing the group name and the noun for the second placeholder (y).
            If empty, the default nouns from the template will be used.
        """
        if self.sentence_style != ROMANTIC_SENTENCE:
            raise ValueError("This method can only be used for romantic sentences.")

        # if xs or ys are empty, use the default ones
        if not xs:
            xs = self.xs
        if not ys:
            ys = self.ys

        instances = []

        for x_group, x, y_group, y in (
            (x_group, x, y_group, y)
            for x_group, x in xs
            for y_group, y in ys
            # only one of the groups has to be of group "romantic"
            if (y_group == "romantic") and x.nom_sg != y.nom_sg
        ):
            # use regex to perform substitutions
            text = re.sub(
                r"<([a-zA-Z_]*)>",
                lambda m: self.resolve(x, y, None, None, m),
                self.sentence,
            )
            # capitalize the first letter of the substitution
            text = text[0].upper() + text[1:]
            # find indices of x and y within the sentence
            x_idx, y_idx = self.find_indices(text, x, y)
            instance = Instance(
                x,
                self.sentence_style,
                self.sentence_id,
                x_group,
                from_none(x_idx),
                y,
                y_group,
                from_none(y_idx),
                None,
                None,
                text,
                None,
                self.statistics,
            )
            instances.append(instance)
        return instances

    def gen_normal(
        self,
        xs: list[tuple[str | int, Noun]] = [],
        ys: list[tuple[str | int, Noun]] = [],
    ) -> list[Instance]:
        """
        Generates instances of the template sentence by replacing placeholders with actual nouns and adjectives.
        This method generates instances for the normal sentence style (1) and the adjective sentence style (2).
        Note that for sentence style 2, _all_ possible combinations will be generated.

        Parameters
        ----------
        xs : list[tuple[str | int, Noun]], optional
            A list of tuples containing the group name and the noun for the first placeholder (x).
            If empty, the default nouns from the template will be used.
        ys : list[tuple[str | int, Noun]], optional
            A list of tuples containing the group name and the noun for the second placeholder (y).
            If empty, the default nouns from the template will be used.
        """
        # if xs or ys are empty, use the default ones
        if not xs:
            xs = self.xs
        if self.sentence_style != NAME_SENTENCE and not ys:
            ys = self.ys

        # Initialize an empty list to store the generated instances
        instances = []

        # For each of our sentence styles, we will use generators to create specific combinations
        # of x, y, adjectives etc. The benefit of using generators is that we can easily limit the number of generated instances
        # without actually generating all of them at once, which is useful for large datasets.

        # yields tuples of the form (x_group, x, y_group, y, adjective, modified)
        # the latter two are unused
        base_generator = (
            (
                x_group,
                x,
                y_group,
                y,
                None,
                None,
            )
            for x_group, x in xs
            for y_group, y in ys
            if x_group != "romantic" and y_group != "romantic"
            if x != y  # make sure we never have the same noun in both x and y
            and self.satisfies_hierarchy(x, y)  # make sure hierarchy is satisfied
            # only consider different gender pairs
            and x.gender != y.gender
            # make sure we never have the same noun in both x and y
            # this is necessary (and different from x != y) because we have nouns like
            # "die Fachkraft" which can be used with multiple genders
            and x.nom_sg != y.nom_sg
        )

        # yields tuples of the form (x_group, x, y_group, y, adjective, modified)
        adjectives_generator = ()
        if self.adjectives:
            adjectives_generator = (
                (
                    x_group,
                    x,
                    y_group,
                    y,
                    adjective,
                    modified,
                )
                for x_group, x in xs
                for y_group, y in ys
                # the same logic as in base_generator, but with adjectives
                if x_group != "romantic" and y_group != "romantic"
                if x != y
                and self.satisfies_hierarchy(x, y)
                and x.gender != y.gender
                and x.nom_sg != y.nom_sg
                for adjective in self.adjectives
                for modified in [
                    "x",
                ]
            )

        for (
            x_group,
            x,
            y_group,
            y,
            adjective,
            modified,
        ) in chain(
            base_generator,
            adjectives_generator,
        ):
            # use regex to perform substitutions
            text = re.sub(
                r"<([a-zA-Z_]*)>",
                lambda m: self.resolve(
                    x,
                    y,
                    adjective,
                    modified,
                    m,
                ),
                self.sentence,
            )
            # capitalize the first letter of the substitution
            text = text[0].upper() + text[1:]
            # find indices of x and y within the sentence
            x_idx, y_idx = self.find_indices(text, x, y)
            instance = Instance(
                x,
                self.sentence_style,
                self.sentence_id,
                x_group,
                from_none(x_idx),
                y,
                y_group,
                None,
                adjective,
                modified,
                text,
                None,
                self.statistics,
            )
            instances.append(instance)

        return instances

    def gen_for_xs(
        self,
        x_group: int | str,
        x_list: list[Noun],
    ) -> list[Instance]:
        """
        Generates instances of the template sentence for a specific noun x.
        This is useful for generating instances for a specific noun without having to generate all instances.

        Parameters
        ----------
        x_group: int | str
            The group of the noun x.
        x_list : list[Noun]
            The noun to generate instances for.
        """
        xs = [(x_group, x) for x in x_list]
        matching_names = []
        if self.sentence_style == NAME_SENTENCE:
            name_sentences = []
            # get names that match gender of x
            for x in x_list:
                if x.gender == "m":
                    matching_names = [
                        name
                        for name in self.names
                        if name.gender == x.gender or name.gender == "n"
                    ]
                elif x.gender == "f":
                    matching_names = [
                        name
                        for name in self.names
                        if name.gender == "f" or name.gender == "n"
                    ]
                else:
                    matching_names = self.names
                matching_names = [random.choice(matching_names)]
                name_sentences.extend(
                    self.gen_name(
                        xs,
                        matching_names,
                    )
                )
            return name_sentences
        else:
            y_group, y_jobs = random.choice(self.ys_by_gender)
            ys = [(y_group, y) for y in y_jobs]

            if self.sentence_style == ROMANTIC_SENTENCE:
                return self.gen_romantic(xs, ys)
            else:
                return self.gen_normal(xs, ys)
