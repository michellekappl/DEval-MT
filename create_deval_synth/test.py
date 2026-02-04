male_names = [name for name in self.names if name.gender == "m"]
female_names = [name for name in self.names if name.gender == "f"]
neutral_names = [name for name in self.names if name.gender == "n"]

# Get jobs by gender (always have male and female, sometimes neutral)
male_jobs = [x for x in x_list if x.gender == "m"]
female_jobs = [x for x in x_list if x.gender == "f"]
neutral_jobs = [x for x in x_list if x.gender == "d"]

# Check if we have both male and female jobs
if not male_jobs or not female_jobs:
    # Skip this group if it doesn't have both
    print(f"  -> Skipping (no male or female jobs)")
    return []

male_job = male_jobs[0]
female_job = female_jobs[0]

# Select one name of each type to use across all combinations
selected_male_name = random.choice(male_names) if male_names else None
selected_neutral_name = random.choice(neutral_names) if neutral_names else None
selected_female_name = random.choice(female_names) if female_names else None

# 1. Male name with male job
if selected_male_name:
name_sentences.extend(
    self.gen_name(
        [(x_group, male_job)],
        [selected_male_name],
    )
)

# 2. Neutral name with male job
if selected_neutral_name:
name_sentences.extend(
    self.gen_name(
        [(x_group, male_job)],
        [selected_neutral_name],
    )
)

# 3. Neutral name with female job
if selected_neutral_name:
name_sentences.extend(
    self.gen_name(
        [(x_group, female_job)],
        [selected_neutral_name],
    )
)

# 4. Female name with female job
if selected_female_name:
name_sentences.extend(
    self.gen_name(
        [(x_group, female_job)],
        [selected_female_name],
    )
)

# If there's a neutral job, add 3 more combinations (total 7)
if neutral_jobs:
neutral_job = neutral_jobs[0]

# 5. Male name with neutral job
if selected_male_name:
    name_sentences.extend(
        self.gen_name(
            [(x_group, neutral_job)],
            [selected_male_name],
        )
    )

# 6. Neutral name with neutral job
if selected_neutral_name:
    name_sentences.extend(
        self.gen_name(
            [(x_group, neutral_job)],
            [selected_neutral_name],
        )
    )

# 7. Female name with neutral job
if selected_female_name:
    name_sentences.extend(
        self.gen_name(
            [(x_group, neutral_job)],
            [selected_female_name],
        )
    )