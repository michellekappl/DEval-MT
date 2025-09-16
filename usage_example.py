import pandas as pd
from Dataset import DEvalDataset
from morphological_analysis.spacy_morph_analyzer import SpaCyMorphAnalyzer
from morphological_analysis.base_analyzer import BaseMorphologicalAnalyzer
from sdk import run_subject_pipeline, evaluate_processed_dataset

def main():
   df = pd.read_csv("full_data.csv", sep=";")
   df = df[df["sentence_style"] == 1][1:25]
   ds = DEvalDataset(df, text_column="text")


   # load translations from a file
   list_of_es_translations = pd.read_csv("translations/es_1.txt", header=None, sep=";")[0].tolist()
   list_of_fr_translations = pd.read_csv("translations/fr_1.txt", header=None, sep=";")[0].tolist()

   # Add translations (must match row count)
   ds.add_translations("es", list_of_es_translations, "es")
   ds.add_translations("fr", list_of_fr_translations, "fr")

   # Build and load analyzers explicitly
   morph_es = SpaCyMorphAnalyzer("es_dep_news_trf"); morph_es.load()
   morph_fr = SpaCyMorphAnalyzer("fr_dep_news_trf"); morph_fr.load()
   analyzers: dict[str, BaseMorphologicalAnalyzer] = {
      "es": morph_es,
      "fr": morph_fr,
   }

   # Run for x subject
   df_x = run_subject_pipeline(
      ds,
   analyzers=analyzers,
      source_column="text",
      subject_index_column="x_idx",
      output_prefix="x",
      article_offset=-1,
      use_multiprocessing=False
   )

   # Persist individual processed variants
   df_x.to_csv("processed_x.csv", sep=";", index=False)

   metrics_x, df_metrics_x = evaluate_processed_dataset(ds.df, ["es","fr"], gold_gender_column="x_gender", output_prefix="x")

   df_metrics_x.to_csv("metrics_x.csv", sep=";", index=False)

if __name__ == '__main__':
   main()


import pandas as pd

pd.read_csv("metrics_x.csv", sep=";")
pd.read_csv("processed_x.csv", sep=";").columns