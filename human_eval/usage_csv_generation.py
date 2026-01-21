from eval_csv_code import create_eval_csv, create_multi_eval_csv

# CHat GPT
# es;fr;it;no;sv;ar;ru;uk

# Google
# es;fr;it;no;sv;ar;ru;uk

# for lang in ["es", "it", "no", "ar"]:
#    create_eval_csv("gpt-4o_processed.csv", lang)

for lang in ["es", "fr", "it", "ar", "he", "ru", "uk"]:
    create_multi_eval_csv(
        lang,
        [
            "google_processed.csv",
            "gpt-4o_processed.csv",
            "systran_processed.csv",
            "deepl_processed.csv",
            "microsoft_processed.csv",
        ],
    )
