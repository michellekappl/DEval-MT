import pandas as pd
import numpy as np
import regex as re


class HumanResults:
    def __init__(self, lang: str, results_id: str = "20260127"):
        self.language = lang
        self.data = self.load_data(results_id)
        self.participants = self.number_of_participants()

    def number_of_participants(self) -> int:
        return len(self.data["match"].iloc[0])  # a bit hacky

    def load_data(self, results_id) -> pd.DataFrame:
        og_data = pd.read_csv(f"results-{results_id}/{self.language}-{results_id}.csv")
        metadata = pd.read_csv(f"outputs/metadata/{self.language}_Multi_hev_metadata_updated.csv", sep=";")

        data_list = []
        for idx in og_data["index"].unique():
            idx_data = og_data[og_data["index"] == idx]

            match_vals = idx_data[idx_data["Question"] == "match"]["Value"].tolist()
            gender_vals = idx_data[idx_data["Question"] == "gender"]["Value"].tolist()
            makesense_vals = idx_data[idx_data["Question"] == "makesense"]["Value"].tolist()

            # Get metadata for this sentence index
            meta_row = metadata[metadata["Index"] == idx]

            if len(meta_row) > 0:
                original_gender = meta_row["Gold_Gender"].iloc[0]
                gender_new_alignment = (
                    meta_row["x_gender_morph"].iloc[0]
                    if "x_gender_morph" in meta_row.columns
                    else None
                )
                gender_old_alignment = (
                    meta_row["x_gender_morph_old"].iloc[0]
                    if "x_gender_morph_old" in meta_row.columns
                    else None
                )
                has_adjective = (
                    meta_row["has_adjective"].iloc[0]
                    if "has_adjective" in meta_row.columns
                    else None
                )
            else:
                original_gender = None
                gender_new_alignment = None
                gender_old_alignment = None
                has_adjective = None

            data_list.append(
                {
                    "index": idx,
                    "translator": idx_data["translator"].iloc[0],
                    "extraction": idx_data["extraction"].iloc[0],
                    "sentence": idx_data["sentence"].iloc[0],
                    "match": match_vals,
                    "gender": gender_vals,
                    "makesense": makesense_vals,
                    "original_gender": original_gender,
                    "gender_new_alignment": gender_new_alignment,
                    "gender_old_alignment": gender_old_alignment,
                    "has_adjective": has_adjective,
                }
            )

        data = pd.DataFrame(data_list)
        return data

    def data_to_csv(self, path: str):
        self.data.to_csv(path, index=False)


for lang in ["es"]:
    results = HumanResults(lang)

    print(f"Language: {lang}, Participants: {results.participants}")
    results.data_to_csv(f"heval_updated_{lang}_results_0127.csv")
