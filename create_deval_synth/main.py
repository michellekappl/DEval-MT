import sys
import csv
import re
from declensions import *
from groups import groups

# open a csv file from argument and read it
if len(sys.argv) < 2:
    print("Usage: python main.py <csv_file>")
    sys.exit(1)


class Template:
    def __init__(self, row):
        self.sentence = row[0]
        self.hierarchy = row[1]
        self.xs = []
        x_groups = row[2].strip("[]").split(",")
        for group in x_groups:
            if group == "":
                # if group is empty, use generic
                group = "generic"
            if group in groups:
                self.xs.extend(groups[group])
            else:
                raise ValueError(f"Unknown group: {group}")

        self.ys = []
        y_groups = row[3].strip("[]").split(",")
        for group in y_groups:
            if group == "":
                # if group is empty, use generic
                group = "generic"
            if group in groups:
                self.ys.extend(groups[group])
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

    def gen(self):
        substitutions = []
        for x, y in [(x, y) for x in self.xs for y in self.ys if x != y]:
            substitution = re.sub(
                r"<([a-zA-Z_]*)>", lambda m: self.resolve(x, y, m), self.sentence
            )
            # capitalize the first letter of the substitution
            substitution = substitution[0].upper() + substitution[1:]
            substitutions.append(substitution)

        return substitutions


csv_file = sys.argv[1]
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    # delete the header
    next(reader)
    for row in reader:
        r = Template(row)
        print(r.gen())
