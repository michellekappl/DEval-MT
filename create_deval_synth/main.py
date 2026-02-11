import random
import sys
import polars as pl

from adjectives import adjectives
from groups import groups
from names import names
from templates import Template
from Instance import Instance

# Set random seed for reproducibility
random.seed(42)


def load_statistics(filepath: str) -> dict[str, dict[str, tuple[int, int]]]:
    """Load job statistics from CSV file."""
    statistics = {}
    # read branchen statistic file
    statistics_csv = pl.read_csv(filepath, separator=";", has_header=True)

    for row in statistics_csv.iter_rows(named=True):
        code = row["Code"]
        status = row["Anforderungsniveau"]
        num_m = 0 if row["Männer"] == "x" else (int(row["Männer"]))
        num_f = 0 if row["Frauen"] == "x" else (int(row["Frauen"]))

        statistics.setdefault(code, {})[status] = (num_m, num_f)

    return statistics


csv_file = 'dataset.csv'

# these are the adjustable parameters:

# number of templates to be randomly selected for each job
GEN_TEMPLATES_PER_JOB = 1
# number of additional instances to be generated for each romantic/name template
GEN_PER_TEMPLATE = 200

# job statistics
statistics = load_statistics("job_statistics/utilities/branchen_statistics.csv")
instances = []
templates = []

reader = pl.read_csv(csv_file, separator=";", has_header=True)

for row in reader.iter_rows(named=True):
    # create template for each row
    r = Template(row, statistics, groups, adjectives, names)
    # generate all instances
    templates.append(r)

print(f"Loaded {len(templates)} templates from {csv_file}.")

# templates that work for any job
generic_templates = [t for t in templates if t.sentence_style == 1 or t.sentence_style == 5]

romantic_templates = [t for t in templates if t.sentence_style == 5]

name_templates = [t for t in templates if t.sentence_style == 6]

pronoun_templates = [t for t in templates if t.sentence_style == 2]

assert (
    len(templates) >= GEN_TEMPLATES_PER_JOB
), "Not enough templates available. Please check the input file."
count = 0
for key, jobs in groups.items():
    # Skip the "romantic" group - it's only used as Y in romantic sentences
    if key == "romantic":
        continue
    for gender_group in jobs:
        count += len(gender_group)
        templates_to_use = random.sample(list(generic_templates), GEN_TEMPLATES_PER_JOB)
        # get the coresponding Pronoun sentences
        pronoun_templates_to_use = []
        for t in templates_to_use:
            for p in pronoun_templates:
                if t.sentence_id == p.sentence_id:
                    pronoun_templates_to_use.append(p)

        # Sample different templates for each job, but ensure BOTH types are included
        romantic_templates_to_use = random.sample(list(romantic_templates), GEN_TEMPLATES_PER_JOB)
        name_templates_to_use = random.sample(list(name_templates), GEN_TEMPLATES_PER_JOB)

        templates_to_use = (
            # templates_to_use
            # + pronoun_templates_to_use
            romantic_templates_to_use
            + name_templates_to_use
        )
        templates_to_use = sorted(templates_to_use, key=lambda template: template.sentence_id)
        for template in templates_to_use:
            instances.extend(template.gen_for_xs(key, gender_group))

print(f"Generated {len(instances)} instances from {len(templates)} templates.")

# Print template usage statistics
print(f"\n{'='*60}")
print("TEMPLATE USAGE STATISTICS")
print(f"{'='*60}")

template_counts = {}
for instance in instances:
    sid = instance.sentence_id
    if sid not in template_counts:
        template_counts[sid] = 0
    template_counts[sid] += 1

# Sort by usage count (descending)
sorted_templates = sorted(template_counts.items(), key=lambda x: x[1], reverse=True)

print(f"{'Sentence ID':<12} {'Count':<8} {'Percentage':<12}")
print("-" * 32)

for sid, count in sorted_templates:
    percentage = (count / len(instances)) * 100
    print(f"{sid:<12} {count:<8} {percentage:>6.2f}%")

print(f"\nTotal instances: {len(instances)}")
print(f"Unique templates used: {len(template_counts)}")
print(f"Average instances per template: {len(instances) / len(template_counts):.1f}")

with open("output.csv", "w", encoding="utf-8") as f:
    # write output file
    n = len(instances)

    f.write(Instance.header + "\n")
    for i, instance in enumerate(instances):
        f.write(str(instance) + "\n")
        print(f"Generating statistics for {n} instances... ({i} / {n})")
        sys.stdout.write("\033[F\033[K")

print(f"Saved {len(instances)} instances.")
