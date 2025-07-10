import sys
import csv
import re
from typing import Any, Generator, Literal
from itertools import islice, cycle


from declensions import *
from groups import groups
from adjectives import adjectives
from names import names


# Remove groups that are not needed for the generation
del groups["other"]
del groups["generic"]


# copied from itertools documentation
# https://docs.python.org/3/library/itertools.html#recipes
def roundrobin(*iterables: Generator[Any]) -> Generator[Any]:
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


# open a csv file from argument and read it
if len(sys.argv) < 2:
    print("Usage: python main.py <csv_file>")
    sys.exit(1)

statistics_file = open("job_statistics/utilities/branchen_statistics.csv", "r")
statistics_csv = csv.reader(statistics_file, delimiter=";")


# helper method to limit the number of items in a generator
def limit(l: int):
    def limiter(gen: Generator[Any]) -> Generator[Any]:
        for _, item in zip(range(l), gen):
            yield item

    return limiter


# extract sentence statistics for lookup of stereotypes
statistics = {}
# read the statistics file and create a dictionary with the groups
for row in statistics_csv:
    if row[0] == "Code":
        continue  # skip header
    code = int(row[0])
    status = row[2]
    num_m = 0 if row[3] == "x" else (int(row[3].replace(".", "")))
    num_f = 0 if row[4] == "x" else (int(row[4].replace(".", "")))

    if statistics.get(code):
        statistics[code][status] = (num_m, num_f)
    else:
        statistics[code] = {}
        statistics[code][status] = (num_m, num_f)


# define constants for sentence styles
NORMAL_SENTENCE = 1
ADJECTIVE_SENTENCE = 2
ROMANTIC_SENTENCE = 3
NAME_SENTENCE = 4


class Instance:
    """
    Represents a single instance of a template sentence.
    Provides string representation in a specific format for CSV output.
    """

    x: Noun
    """The first noun in the sentence."""
    x_group: str
    """The group of the first noun (either "romantic" or a number corresponding to some job group)."""
    x_idx: int
    """The index of the first noun in the sentence (where "," is counted as a separate token)."""
    y: Noun | None
    """The second noun in the sentence, or None if this is a name sentence."""
    y_group: str | None
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

    def __init__(
        self,
        x: Noun,
        x_group: str,
        x_idx: int,
        y: Noun,
        y_group: str,
        y_idx: int,
        adjective: Adjective | None,
        modified: str | None,
        text: str,
        name: Name | None,
    ):
        self.x = x
        self.y = y
        self.x_group = x_group
        self.y_group = y_group
        self.text = text
        self.adjective = adjective
        self.modified = modified  # "x" or "y", which one was modified
        self.x_idx = x_idx  # index of x in the sentence
        self.y_idx = y_idx  # index of y in the sentence
        self.name = name

    header = (
        "sentence_style;"
        "x_nom_sg;x_group;x_gender;x_idx;x_stereotypical;x_level;"
        "y_nom_sg;y_group;y_gender;y_idx;y_stereotypical;y_level;"
        "adjective;modified;name;name.gender;text"
    )
    """The header for the CSV file, describing the fields in the same order as they are in the string representation."""

    def __str__(self):
        return (
            f"{self.sentence_style};"
            + f"{self.x.nom_sg};{self.x_group};{self.x.gender};{self.x_idx};{self.x_stereotypical};{self.x.status or "none"};"
            + (
                f"{self.y.nom_sg};{self.y_group};{self.y.gender};{self.y_idx};{self.y_stereotypical};{self.y.status or "none"};"
                if self.y
                else "none;none;none;none;none;none;"
            )
            + f"{self.adjective.text if self.adjective else 'none'};"
            + f"{self.modified or 'none'};"
            + (f"{self.name.text};{self.name.gender};" if self.name else "none;none;")
            + f"{self.text}"
        )

    @property
    def sentence_style(self) -> Literal[4, 3, 2, 1]:
        """The style of the sentence, one of the constants defined above.
        - NAME_SENTENCE (4) if this is a name sentence (i.e. y is None),
        - ROMANTIC_SENTENCE (3) if either x or y is in the romantic group,
        - ADJECTIVE_SENTENCE (2) if there is an adjective inserted into the sentence,
        - NORMAL_SENTENCE (1) otherwise.
        """
        if self.y is None:
            return NAME_SENTENCE
        elif self.x_group == "romantic" or self.y_group == "romantic":
            return ROMANTIC_SENTENCE
        elif self.adjective:
            return ADJECTIVE_SENTENCE
        else:
            return NORMAL_SENTENCE

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
            num_m, num_f = statistics[self.x_group][self.x.status]
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
        if (
            self.sentence_style == NAME_SENTENCE
            or self.sentence_style == ROMANTIC_SENTENCE
        ):
            return float("nan")
        else:
            num_m, num_f = statistics[self.y_group][self.y.status]
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

    GEN_LIMIT = 1000
    """Limit for the number of generated instances per template."""

    def __init__(
        self,
        row: list[str],
        groups: dict[str | int, list[Noun]] = groups,
        adjectives: list[Adjective] = adjectives,
    ):
        """
        Initializes the template with a sentence, hierarchy, and groups of nouns.

        Parameters
        ----------
        row : list[str]
            A list containing the sentence template, hierarchy, and groups of nouns.
        groups : dict[str | int, list[Noun]], optional
            A dictionary mapping group names or numbers to lists of nouns. Defaults to the global `groups`.
        adjectives : list[Adjective], optional
            A list of adjectives to use in the template. Defaults to the global `adjectives`.
        """

        self.sentence = row[0].strip()  # the actual sentence template
        self.adjectives = adjectives  # adjectives to use in template
        self.groups = groups  # groups to use in template

        # the hierarchy of the template, i.e. "x>y", "x<y" or "none"
        hierarchy = row[1].strip()
        self.higher = None  # the higher group in the hierarchy, either "x" or "y", or None if no hierarchy is defined

        # parse hierarchy
        if hierarchy != "none":
            if ">" in hierarchy or "<" in hierarchy:
                # check that the hierarchy variable is x or y
                if hierarchy[0] in ("x", "y"):
                    self.higher = hierarchy[0]
                else:
                    raise ValueError(f"Invalid hierarchy: {hierarchy}")
            else:
                raise ValueError(f"Invalid hierarchy: {hierarchy}")

        # add all the relevant jobs to the xs list
        # the xs list is of the form [(group_id, Noun), ...]
        self.xs: list[tuple[str | int, Noun]] = []
        # parse x groups from the row (this is a string of the form '[111, "romantic", 333]')
        x_groups = row[2].strip("[]").split(",")
        for group in x_groups:
            if group == "":
                # if the group array is empty, add all groups except "romantic"
                for g in groups:
                    if g != "romantic":
                        self.xs.extend(map(lambda x: (g, x), groups[g]))
            elif group == "romantic":
                # find the romantic group and add it
                # note that the mapping is necessary to keep track of the group name
                self.xs.extend(map(lambda x: ("romantic", x), groups["romantic"]))
            elif int(group) in groups:
                # see above
                self.xs.extend(map(lambda x: (int(group), x), groups[int(group)]))
            else:
                raise ValueError(f"Unknown group: {group}")

        # check if there is a <y> value in the sentence
        # if not, then this is a name (style 4) sentence
        self.sentence_style = NAME_SENTENCE if self.sentence.find("<y") == -1 else None

        # otherwise, do exactly the same for ys
        if self.sentence_style != NAME_SENTENCE:
            self.ys = []
            y_groups = row[3].strip("[]").split(",")
            for group in y_groups:
                if group == "":
                    # if group is empty, add all groups
                    for g in groups:
                        if g != "romantic":
                            self.ys.extend(map(lambda x: (g, x), groups[g]))
                elif group == "romantic":
                    self.ys.extend(map(lambda x: ("romantic", x), groups["romantic"]))
                elif int(group) in groups:
                    self.ys.extend(map(lambda x: (int(group), x), groups[int(group)]))
                else:
                    raise ValueError(f"Unknown group: {group}")

    def resolve_name(self, x: Noun, name: Noun, match: re.Match) -> str:
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

        if parts[1] in ["nom", "gen", "dat", "acc"]:
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
            else:
                # case where gender is not known, so we need to use the other noun to determine it
                # something like <x_poss_acc>
                other_noun = y if parts[0] == "x" else x  # complement to base_noun
                case = parts[2]
                return Possessive(base_noun, other_noun.grammatical_gender).decline(
                    case, "sg"
                )
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
        If the hierarchy is None, returns True.
        """
        if self.higher is None:
            return True
        elif not hasattr(x, "status") or not hasattr(y, "status"):
            # if x or y do not have a status, we cannot compare them
            return False

        status_lookup = {
            "Experten": 4,
            "Spezialisten": 3,
            "Fachkräfte": 2,
            "Helfer": 1,
        }
        if self.higher == "x":
            return status_lookup[x.status] > status_lookup[y.status]
        elif self.higher == "y":
            return status_lookup[x.status] < status_lookup[y.status]
        else:
            raise ValueError(f"Invalid hierarchy: {self.higher}")

    def gen(self) -> list[Instance]:
        """
        Generates instances of the template sentence by replacing placeholders with actual nouns and adjectives.
        This is where the main logic of the template generation happens.
        """

        # Initialize an empty list to store the generated instances
        instances = []

        # For each of our sentence styles, we will use generators to create specific combinations
        # of x, y, adjectives etc. The benefit of using generators is that we can easily limit the number of generated instances
        # without actually generating all of them at once, which is useful for large datasets.

        # yields tuples of the form (x_group, x, y_group, y, adjective, modified)
        # the latter two are unused
        base_generator = (
            (x_group, x, y_group, y, None, None)
            for x_group, x in self.xs
            for y_group, y in self.ys
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
                (x_group, x, y_group, y, adjective, modified)
                for x_group, x in self.xs
                for y_group, y in self.ys
                # the same logic as in base_generator, but with adjectives
                if x_group != "romantic" and y_group != "romantic"
                if x != y
                and self.satisfies_hierarchy(x, y)
                and x.gender != y.gender
                and x.nom_sg != y.nom_sg
                for adjective in self.adjectives
                for modified in ["x", "y"]
            )

        # yields tuples of the form (x_group, x, y_group, y, adjective, modified)
        # the latter two are unused
        romantic_generator = (
            (x_group, x, y_group, y, None, None)
            for x_group, x in self.xs
            for y_group, y in self.ys
            # only one of the groups has to be of group "romantic"
            if (x_group == "romantic" or y_group == "romantic") and x.nom_sg != y.nom_sg
        )

        # yields tuples of the form (x_group, x, name)
        names_generator = (
            (x_group, x, name)
            for x_group, x in self.xs
            for name in names
            if name.gender == x.gender or name.gender == "n"
        )

        if self.sentence_style == NAME_SENTENCE:
            # if this is a name sentence, we only need to generate instances with names
            for x_group, x, name in limit(self.GEN_LIMIT)(names_generator):
                # use regex to perform substitutions
                text = re.sub(
                    r"<([a-zA-Z_]*)>",
                    lambda m: self.resolve_name(x, name, m),
                    self.sentence,
                )
                # capitalize the first letter of the substitution
                text = text[0].upper() + text[1:]

                # find index for x
                x_idx = None

                for idx, word in enumerate(
                    text.replace(",", " ,").replace(".", " .").split()
                ):
                    if word in [
                        x.nom_sg,
                        x.gen_sg,
                        x.dat_sg,
                        x.acc_sg,
                        # plurals are unused so far, so we can skip this
                        # x.nom_pl,
                        # x.gen_pl,
                        # x.dat_pl,
                        # x.acc_pl,
                    ]:
                        x_idx = idx
                        # break after first occurance
                        break

                # create instance with the determined paramters
                instance = Instance(
                    x, x_group, x_idx, None, None, None, None, None, text, name
                )
                # add to list of all instances
                instances.append(instance)
        else:
            for x_group, x, y_group, y, adjective, modified in limit(self.GEN_LIMIT)(
                # use roundrobin to make sure we get all sentence styles no matter how low the limit
                roundrobin(base_generator, adjectives_generator, romantic_generator)
            ):
                # use regex to perform substitutions
                text = re.sub(
                    r"<([a-zA-Z_]*)>",
                    lambda m: self.resolve(x, y, adjective, modified, m),
                    self.sentence,
                )
                # capitalize the first letter of the substitution
                text = text[0].upper() + text[1:]

                # find indices of x and y within the sentence
                x_idx, y_idx = None, None
                for idx, word in enumerate(
                    text.replace(",", " ,").replace(".", " .").split()
                ):
                    if word in [
                        x.nom_sg,
                        x.gen_sg,
                        x.dat_sg,
                        x.acc_sg,
                        # x.nom_pl,
                        # x.gen_pl,
                        # x.dat_pl,
                        # x.acc_pl,
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

                instance = Instance(
                    x,
                    x_group,
                    x_idx,
                    y,
                    y_group,
                    y_idx,
                    adjective,
                    modified,
                    text,
                    None,
                )
                instances.append(instance)

        return instances


instances = []
csv_file = sys.argv[1]

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    # delete the header
    next(reader)
    for row in reader:
        # create template for each row
        r = Template(row)
        # generate all instances
        gen = r.gen()
        instances.extend(r.gen())

        # give some progress indication
        print(f"Generated {len(gen)} instances for template: {r.sentence}")
        # delete the progress indication for every iteration
        sys.stdout.write("\033[F\033[K")
with open("output.csv", "w", encoding="utf-8") as f:
    # write output file
    n = len(instances)

    f.write(Instance.header + "\n")

    for i, instance in enumerate(instances):
        f.write(str(instance) + "\n")
        print(f"Generating statistics for {n} instances... ({i} / {n})")
        sys.stdout.write("\033[F\033[K")

print(f"Generated {len(instances)} instances.")
