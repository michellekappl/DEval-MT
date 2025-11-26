import csv
import random
import sys

from adjectives import adjectives
from groups import groups
from names import names
from templates import (
    NAME_SENTENCE,
    NORMAL_SENTENCE,
    ROMANTIC_SENTENCE,
    Instance,
    Template,
)

# Remove groups that are not needed for the generation
# del groups["other"]
# del groups["generic"]


def load_statistics(filepath: str) -> dict[str, dict[str, tuple[int, int]]]:
    """Load job statistics from CSV file."""
    statistics = {}
    with open(filepath, "r") as statistics_file:
        statistics_csv = csv.reader(statistics_file, delimiter=";")
        for row in statistics_csv:
            if row[0] == "Code":
                continue  # skip header
            code = int(row[0])
            status = row[2]
            num_m = 0 if row[3] == "x" else (int(row[3].replace(".", "")))
            num_f = 0 if row[4] == "x" else (int(row[4].replace(".", "")))

            statistics.setdefault(code, {})[status] = (num_m, num_f)

    return statistics


# parse command line arguments
if len(sys.argv) < 2:
    print("Usage: python main.py <csv_file>")
    sys.exit(1)

csv_file = sys.argv[1]

# these are the adjustable parameters:

# number of templates to be randomly selected for each job
GEN_TEMPLATES_PER_JOB = 2
# number of additional instances to be generated for each romantic/name template
GEN_PER_TEMPLATE = 100

# job statistics
statistics = load_statistics("job_statistics/utilities/branchen_statistics.csv")
instances = []
templates = []


with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    # delete the header
    next(reader)
    for row in reader:
        # create template for each row
        r = Template(row, statistics, groups, [], names)
        # generate all instances
        templates.append(r)

print(f"Loaded {len(templates)} templates from {csv_file}.")

# templates that work for any job
generic_templates = [
    t for t in templates if t.generic and t.sentence_style == NORMAL_SENTENCE
]

assert len(templates) >= GEN_TEMPLATES_PER_JOB, (
    "Not enough templates available. Please check the input file."
)

for key, jobs in groups.items():
    # select templates based on the group key
    specific_templates = [t for t in templates if key in t.matching_x_groups]

    # romantic groups are handled separately
    if key == "romantic" and len(specific_templates) < GEN_TEMPLATES_PER_JOB:
        continue
    else:
        for gender_group in jobs:
            generic_templates_to_use = (
                []
                if len(specific_templates) >= GEN_TEMPLATES_PER_JOB
                else random.sample(
                    list(generic_templates),
                    GEN_TEMPLATES_PER_JOB - len(specific_templates),
                )
            )
            # use all generic templates
            templates_to_use = list(specific_templates) + generic_templates_to_use

            for template in templates_to_use:
                instances.extend(template.gen_for_xs(key, gender_group))

for template in filter(
    lambda t: t.sentence_style in [NAME_SENTENCE, ROMANTIC_SENTENCE], templates
):
    # make sure we have generate sentences with names and romantic groups
    xs = random.sample(template.xs, GEN_PER_TEMPLATE)
    for x_group, x in xs:
        instances.extend(template.gen_for_xs(x_group, [x]))

print(f"Generated {len(instances)} instances from {len(templates)} templates.")
with open("output.csv", "w", encoding="utf-8") as f:
    # write output file
    n = len(instances)

    f.write(Instance.header + "\n")

    for i, instance in enumerate(instances):
        f.write(str(instance) + "\n")
        print(f"Generating statistics for {n} instances... ({i} / {n})")
        sys.stdout.write("\033[F\033[K")

print(f"Saved {len(instances)} instances.")