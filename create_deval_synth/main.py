import sys
import csv
import re
from declensions import *
from groups import groups

# open a csv file from argument and read it
if len(sys.argv) < 2:
    print("Usage: python main.py <csv_file>")
    sys.exit(1)

statistics_file = open("job_statistics/utilities/branchen_statistics.csv", "r")
statistics_csv = csv.reader(statistics_file, delimiter=";")

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


class Instance:
    def __init__(self, x, x_group, y, y_group, text):
        self.x = x
        self.y = y
        self.x_group = x_group
        self.y_group = y_group
        self.text = text

    def __str__(self):
        return f"{self.x.nom_sg}, {self.y.nom_sg} ({self.x_group}, {self.y_group}): {self.text}, x_stereotypical: {self.x_stereotypical()}, y_stereotypical: {self.y_stereotypical()}"

    def x_stereotypical(self):
        num_m, num_f = statistics[self.x_group][self.x.status]
        if self.x.gender == "m":
            return num_m > 0.7 * (num_m + num_f)
        elif self.x.gender == "f":
            return num_f > 0.7 * (num_m + num_f)
        else:
            return False

    def y_stereotypical(self):
        num_m, num_f = statistics[self.y_group][self.y.status]
        if self.y.gender == "m":
            return num_m > 0.7 * (num_m + num_f)
        elif self.y.gender == "f":
            return num_f > 0.7 * (num_m + num_f)
        else:
            return False


class Template:
    def __init__(self, row):
        self.sentence = row[0].strip()
        hierarchy = row[1].strip()
        self.higher = None
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
                    self.xs.extend(map(lambda x: (g, x), groups[g]))
            elif int(group) in groups:
                self.xs.extend(map(lambda x: (int(group), x), groups[int(group)]))
            else:
                raise ValueError(f"Unknown group: {group}")

        self.ys = []
        y_groups = row[3].strip("[]").split(",")
        for group in y_groups:
            if group == "":
                # if group is empty, add all groups
                for g in groups:
                    self.ys.extend(map(lambda x: (g, x), groups[g]))
            elif int(group) in groups:
                self.ys.extend(map(lambda x: (int(group), x), groups[int(group)]))
            else:
                raise ValueError(f"Unknown group: {group}")

    def resolve(self, x, y, match):
        # split match by underscores
        parts = match.group(1).split("_")

        base_noun = x if parts[0] == "x" else y

        if parts[1] in ["nom", "gen", "dat", "acc"]:
            # case that this is a simply a definite noun phrase
            return Definite(base_noun).decline(parts[1], "sg")
        elif parts[1] == "rel":
            return Relative(base_noun).decline(parts[2], "sg")
        elif parts[1] == "pron":
            return Pronoun(base_noun).decline(parts[2], "sg")
        elif parts[1] == "poss":
            return Possessive(base_noun, parts[2]).decline(parts[3], "sg")
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
        for (x_group, x), (y_group, y) in [
            (x, y)
            for x in self.xs
            for y in self.ys
            if x != y and self.satisfies_hierarchy(x[1], y[1])
        ]:
            text = re.sub(r"<([a-zA-Z_]*)>", lambda m: self.resolve(x, y, m), self.sentence)
            # capitalize the first letter of the substitution
            text = text[0].upper() + text[1:]
            instance = Instance(x, x_group, y, y_group, text)
            instances.append(instance)

        return instances


instances = []
csv_file = sys.argv[1]
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    # delete the header
    next(reader)
    for row in reader:
        r = Template(row)
        gen = r.gen()
        instances.extend(r.gen())
with open("output.txt", "w", encoding="utf-8") as f:
    for instance in instances:
        f.write(str(instance) + "\n")
        print(str(instance))  # also print to console
print(f"Generated {len(instances)} instances.")
