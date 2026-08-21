import pandas as pd

# === Beschäftigungszahlen ===
df_branchen = pd.read_csv("branchen_statistics.csv", sep=';', converters={'Code': str})
# === Berufscodes mit Beschreibungen ===
df_jobs = pd.read_csv("job_titles.csv", sep=';', converters={'Code': str})
df_jobs = df_jobs.map(lambda x: x.strip() if isinstance(x, str) else x)
df_jobs['3_digit_code'] = df_jobs['Code'].str[:3]

# === Codes mit hoher Auflösung ===
df_decoder = pd.read_csv("decoder.csv", sep=';', converters={'Code': str})
df_decoder = df_decoder.map(lambda x: x.strip() if isinstance(x, str) else x)

# === add Niveau to df_jobs ===
df_jobs = df_jobs.merge(df_decoder[['Code', 'Niveau', 'Misc']], on='Code', how='left')

# === merge df_jobs with df_branchen ===
df_branchen = df_branchen.rename(columns={"Code": "3_digit_code", "Anforderungsniveau": "Niveau"})

# === Merge durchführen auf Code + Niveau ===
df_merged = pd.merge(df_jobs, df_branchen, on=["3_digit_code", "Niveau"], how="left")

# === group by branchen ===
df_branchen_with_jobs = (
    df_merged.groupby(["3_digit_code", "Name","Niveau", "Männer", "Frauen"])
          .agg(Berufe=("Bezeichnung", list))
          .reset_index()
)
df_branchen_with_jobs['Berufe'] = df_branchen_with_jobs['Berufe'].apply(lambda x: list(set(x)))
df_branchen_with_jobs.to_csv("../branchen_with_jobs.csv", sep=';', index=False)

# === load branchen with jobs ===
df_branchen_with_jobs = pd.read_csv("../branchen_with_jobs.csv", sep=';', converters={'3_digit_code': str})

# === create lookup table for main categories ===
df_main_categories = (df_decoder[df_decoder['Code'].astype(str).str.len() == 1]).reset_index(drop=True).drop(columns=['Niveau', 'Misc'])
df_branchen_with_jobs["1_digit_code"] = df_branchen_with_jobs["3_digit_code"].str[0]
df_copy = df_branchen_with_jobs[['3_digit_code', '1_digit_code']].copy().rename(columns={"1_digit_code": "Code"}).drop_duplicates().reset_index(drop=True)
df_main_categories = df_main_categories.merge(df_copy, on="Code", how="left").rename(columns={"Bezeichnung": "main_branche"})
df_main_categories = df_main_categories.groupby(["Code", "main_branche"]).agg(corresponding_jobs=("3_digit_code", list))
print()
df_main_categories.to_csv("../main_branchen.csv", sep=';')
