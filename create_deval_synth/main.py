import sys
import csv
import re
from declensions import *
from groups import groups
from adjectives import adjectives
from names import names


from itertools import islice, cycle

del groups["other"]
del groups["generic"]


# copied from itertools documentation
# https://docs.python.org/3/library/itertools.html#recipes
def roundrobin(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


GEN_LIMIT = 1000  # limit the number of generated instances per template

# open a csv file from argument and read it
if len(sys.argv) < 2:
    print("Usage: python main.py <csv_file>")
    sys.exit(1)

statistics_file = open("job_statistics/utilities/branchen_statistics.csv", "r")
statistics_csv = csv.reader(statistics_file, delimiter=";")


# helper method to limit the number of items in a generator
def limit(l):
    def limiter(gen):
        for _, item in zip(range(l), gen):
            yield item

    return limiter


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
    def __init__(
        self,
        x,
        x_group,
        x_idx,
        y,
        y_group,
        y_idx,
        adjective,
        modified,
        text,
        name,
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

    header = "sentence_style;x_nom_sg;x_group;x_gender;x_idx;x_stereotypical;x_level;y_nom_sg;y_group;y_gender;y_idx;y_stereotypical;y_level;adjective;modified;name;name.gender;text"

    def __str__(self):
        return (
            f"{self.sentence_style};"
            + f"{self.x.nom_sg};{self.x_group};{self.x.gender};{self.x_idx};{self.x_stereotypical};{self.x.status or "none"};"
            + (
                f"{self.y.nom_sg};{self.y_group};{self.y.gender};{self.y_idx};{self.y_stereotypical};{self.y.status or "none"};"
                if self.y
                else "none;none;none;"
            )
            + f"{self.adjective.text if self.adjective else 'none'};"
            + f"{self.modified or 'none'};"
            + (f"{self.name.text};{self.name.gender};" if self.name else "none;none;")
            + f"{self.text}"
        )

    @property
    def sentence_style(self):
        if self.y is None:
            return NAME_SENTENCE
        elif self.x_group == "romantic" or self.y_group == "romantic":
            return ROMANTIC_SENTENCE
        elif self.adjective:
            return ADJECTIVE_SENTENCE
        else:
            return NORMAL_SENTENCE

    @property
    def x_stereotypical(self):
        if self.sentence_style == NAME_SENTENCE:
            return "none"

        if self.x_group == "romantic":
            return "romantic"

        num_m, num_f = statistics[self.x_group][self.x.status]
        if num_m == 0 and num_f == 0:
            return "none"
        if self.x.gender == "m":
            return num_m / (num_m + num_f)
        elif self.x.gender == "f":
            return num_f / (num_m + num_f)
        else:
            return "none"

    @property
    def y_stereotypical(self):
        if self.sentence_style == NAME_SENTENCE:
            return "none"

        if self.y_group == "romantic":
            return "romantic"
        else:
            num_m, num_f = statistics[self.y_group][self.y.status]
            if num_m == 0 and num_f == 0:
                return "no data"
            if self.y.gender == "m":
                return num_m / (num_m + num_f)
            elif self.y.gender == "f":
                return num_f / (num_m + num_f)
            else:
                return "none"


class Template:
    def __init__(self, row, adjectives=None):
        self.sentence = row[0].strip()
        hierarchy = row[1].strip()
        self.adjectives = adjectives
        self.higher = None

        self.type = "name_sentences" if self.sentence.find("<y") == -1 else "other"

        # parse hierarchy
        if hierarchy != "none":
            if hierarchy.find(">"):
                hierarchy = hierarchy.split(">")
                if hierarchy[0] == "x":
                    self.higher = "x"
                elif hierarchy[0] == "y":
                    self.higher = "y"
            elif hierarchy.find("<"):
                hierarchy = hierarchy.split("<")
                if hierarchy[0] == "x":
                    self.higher = "x"
                elif hierarchy[0] == "y":
                    self.higher = "y"
            else:
                raise ValueError(f"Unknown hierarchy format: {hierarchy}")
        self.xs = []
        x_groups = row[2].strip("[]").split(",")
        for group in x_groups:
            if group == "":
                # if group is empty, add all groups
                for g in groups:
                    if g != "romantic":
                        self.xs.extend(map(lambda x: (g, x), groups[g]))
            elif group == "romantic":
                self.xs.extend(map(lambda x: ("romantic", x), groups["romantic"]))
            elif int(group) in groups:
                self.xs.extend(map(lambda x: (int(group), x), groups[int(group)]))
            else:
                raise ValueError(f"Unknown group: {group}")

        if self.type != "name_sentences":
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

    def resolve_name(self, x, name, match):
        parts = match.group(1).split("_")

        if parts[0] == "x":
            return x.decline(parts[1], "sg")
        elif parts[0] == "name":
            # we only have nominative case in our dataset for names
            return name.decline("nom", "sg")

    def resolve(self, x, y, adjective, modified, match):
        # split match by underscores
        parts = match.group(1).split("_")

        base_noun = x if parts[0] == "x" else y

        if parts[1] in ["nom", "gen", "dat", "acc"]:
            # case that this is a simply a definite noun phrase
            if adjective and parts[0] == modified:
                # if we have an adjective and the noun is the modified one, use it
                return Definite(base_noun, adjective).decline(parts[1], "sg")
            else:
                return Definite(base_noun).decline(parts[1], "sg")
        elif parts[1] == "rel":
            return Relative(base_noun).decline(parts[2], "sg")
        elif parts[1] == "pron":
            return Pronoun(base_noun).decline(parts[2], "sg")
        elif parts[1] == "poss":
            if len(parts) == 4:
                # this is the case where we know the gender of the possessed noun (i.e. it doesn't change)
                return Possessive(base_noun, parts[2]).decline(parts[3], "sg")
            else:
                other_noun = y if parts[0] == "x" else x
                return Possessive(base_noun, other_noun.grammatical_gender).decline(
                    parts[2], "sg"
                )
        elif parts[1] == "indef":
            return base_noun.decline(parts[2], "sg")
        else:
            # throw error
            raise ValueError(f"Unknown match type: {parts}")

    def satisfies_hierarchy(self, x, y):
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

    def gen(self):
        instances = []

        base_generator = (
            (x_group, x, y_group, y, None, None)
            for x_group, x in self.xs
            for y_group, y in self.ys
            if x_group != "romantic" and y_group != "romantic"
            if x != y
            and self.satisfies_hierarchy(x, y)
            and x.gender != y.gender
            and x.nom_sg != y.nom_sg
        )

        adjectives_generator = ()
        if self.adjectives != None:
            adjectives_generator = (
                (x_group, x, y_group, y, adjective, modified)
                for x_group, x in self.xs
                for y_group, y in self.ys
                if x_group != "romantic" and y_group != "romantic"
                if x != y
                and self.satisfies_hierarchy(x, y)
                and x.gender != y.gender
                and x.nom_sg != y.nom_sg
                for adjective in self.adjectives
                for modified in ["x", "y"]
            )

        romantic_generator = (
            (x_group, x, y_group, y, None, None)
            for x_group, x in self.xs
            for y_group, y in self.ys
            if x_group == "romantic" or y_group == "romantic" and x.nom_sg != y.nom_sg
        )

        names_generator = (
            (x_group, x, name)
            for x_group, x in self.xs
            for name in names
            if name.gender == x.gender or name.gender == "n"
        )

        if self.type == "name_sentences":
            for x_group, x, name in limit(GEN_LIMIT)(names_generator):
                text = re.sub(
                    r"<([a-zA-Z_]*)>",
                    lambda m: self.resolve_name(x, name, m),
                    self.sentence,
                )
                # capitalize the first letter of the substitution
                text = text[0].upper() + text[1:]

                x_idx = None
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

                instance = Instance(
                    x, x_group, x_idx, None, None, None, None, None, text, name
                )
                instances.append(instance)
        else:
            for x_group, x, y_group, y, adjective, modified in limit(GEN_LIMIT)(
                roundrobin(base_generator, adjectives_generator, romantic_generator)
            ):
                text = re.sub(
                    r"<([a-zA-Z_]*)>",
                    lambda m: self.resolve(x, y, adjective, modified, m),
                    self.sentence,
                )
                # capitalize the first letter of the substitution
                text = text[0].upper() + text[1:]

                x_idx, y_idx = None, None
                # find idx of x and y within the sentence
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
        r = Template(row, adjectives=adjectives)
        gen = r.gen()
        instances.extend(r.gen())
        # give some progress indication
        print(f"Generated {len(gen)} instances for template: {r.sentence}")
        # delete the progress indication for every iteration
        sys.stdout.write("\033[F\033[K")
with open("output.csv", "w", encoding="utf-8") as f:
    n = len(instances)
    f.write(Instance.header + "\n")
    for i, instance in enumerate(instances):
        f.write(str(instance) + "\n")
        print(f"Generating statistics for {n} instances... ({i} / {n})")
        sys.stdout.write("\033[F\033[K")

print(f"Generated {len(instances)} instances.")
