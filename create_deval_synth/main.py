import csv
import random
import sys
from itertools import cycle, islice

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
        r = Template(row, statistics, groups, adjectives, names)
        # generate all instances
        templates.append(r)

print(f"Loaded {len(templates)} templates from {csv_file}.")

# templates that work for any job - filter by generic flag and sentence style
# Only use normal and normal_pron templates (not romantic or name templates)
generic_normal_templates = [t for t in templates if t.generic and t.sentence_style in [1, 2]]

print(f"Found {len(generic_normal_templates)} generic templates (normal + normal_pron)")

# Group templates by sentence_id to match normal with normal_pron versions
templates_by_id = {}
for t in generic_normal_templates:
    if t.sentence_id not in templates_by_id:
        templates_by_id[t.sentence_id] = []
    templates_by_id[t.sentence_id].append(t)

print(f"Available sentence IDs: {sorted(templates_by_id.keys())}")
for sid, temps in sorted(templates_by_id.items()):
    print(f"  ID {sid}: {len(temps)} templates, styles: {[t.sentence_style for t in temps]}")

assert (
    len(templates_by_id) >= GEN_TEMPLATES_PER_JOB
), f"Not enough generic template pairs available. Found {len(templates_by_id)}, need at least {GEN_TEMPLATES_PER_JOB}."

print(f"\n{'='*60}")
print(f"GENERATING INSTANCES (GEN_TEMPLATES_PER_JOB = {GEN_TEMPLATES_PER_JOB})")
print(f"{'='*60}")

# Create a cycle through template IDs to ensure balanced usage
template_ids = list(templates_by_id.keys())
template_cycle = cycle(template_ids)

for key, jobs in groups.items():
    # select templates based on the group key
    all_specific_templates = [t for t in templates if key in t.matching_x_groups]

    print(f"\n{'='*60}")
    print(f"GROUP: '{key}' (has {len(jobs)} gender groups)")
    print(f"{'='*60}")
    print(f"Found {len(all_specific_templates)} specific templates for this group")

    # romantic groups are handled separately
    if key == "romantic" and len(all_specific_templates) < GEN_TEMPLATES_PER_JOB:
        print(f"  ⚠️  SKIPPING romantic group (not enough specific templates)")
        continue
    else:
        for idx, gender_group in enumerate(jobs):
            print(f"\n  --- Gender group {idx + 1}/{len(jobs)} (has {len(gender_group)} jobs) ---")

            # Get next GEN_TEMPLATES_PER_JOB template IDs from cycle (ensures balanced usage)
            selected_ids = list(islice(template_cycle, GEN_TEMPLATES_PER_JOB))
            print(f"  Selected sentence IDs: {selected_ids}")

            # Get all templates (both normal and normal_pron) for selected IDs
            templates_to_use = []
            for sid in selected_ids:
                templates_to_use.extend(templates_by_id[sid])
                print(f"    ID {sid}: added {len(templates_by_id[sid])} templates")

            templates_to_use = sorted(templates_to_use, key=lambda template: template.sentence_id)
            print(f"  Total templates to use: {len(templates_to_use)}")

            instances_before = len(instances)
            for template in templates_to_use:
                try:
                    new_instances = template.gen_for_xs(key, gender_group)
                    instances.extend(new_instances)

                    # Only print details if 0 instances generated
                    if len(new_instances) == 0:
                        print(
                            f"    ⚠️  Template {template.sentence_id} (style {template.sentence_style}): 0 INSTANCES"
                        )
                        print(
                            f"        - template.ys_by_gender: {len(template.ys_by_gender)} entries"
                        )
                        if template.ys_by_gender:
                            groups = [g for g, _ in template.ys_by_gender]
                            print(f"        - groups in ys_by_gender: {set(groups)}")
                            non_romantic = [g for g in groups if g != "romantic"]
                            print(f"        - non-romantic groups: {len(non_romantic)}")
                    else:
                        print(
                            f"    Template {template.sentence_id} (style {template.sentence_style}): {len(new_instances)} instances ✓"
                        )
                except Exception as e:
                    import traceback

                    print(
                        f"    Template {template.sentence_id}: ❌ ERROR - {type(e).__name__}: {e}"
                    )
                    traceback.print_exc()

            instances_generated = len(instances) - instances_before
            print(f"  ✓ Total for gender group: {instances_generated}")

# for template in filter(
#     lambda t: t.sentence_style in [NAME_SENTENCE, ROMANTIC_SENTENCE], templates
# ):
#     # make sure we have generate sentences with names and romantic groups
#     xs = random.sample(template.xs, GEN_PER_TEMPLATE)
#     for x_group, x in xs:
#         if template.sentence_style == NAME_SENTENCE and x_group == "romantic":
#             continue
#         else:
#             instances.extend(template.gen_for_xs(x_group, [x]))

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
    neutral_marker = 0
    for i, instance in enumerate(instances):
        if neutral_marker == 1 and instance.x.gender == "d":
            neutral_marker = 0
            n -= 1
            continue  # skip every second neutral instance to avoid overrepresentation
        if instance.x.gender == "d" and neutral_marker == 0:
            neutral_marker = 1
        f.write(str(instance) + "\n")
        print(f"Generating statistics for {n} instances... ({i} / {n})")
        sys.stdout.write("\033[F\033[K")
print(f"Saved {n} instances.")
