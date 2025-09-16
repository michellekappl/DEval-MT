evaluator = GenderBiasEvaluator("data_huge.csv")
sentences = evaluator.get_source_sentences()
evaluator.export_sentences("sentences.txt")
# DEval-MT (SDK only)

Python SDK to evaluate gender in MT outputs using alignment + morphological analyzers.

## Install

```bash
pip install -e .
python -m spacy download es_dep_news_trf
python -m spacy download fr_dep_news_trf
```

## Minimal usage

```python
import pandas as pd
from deval_mt import (
  DEvalDataset,
  run_subject_pipeline,
  evaluate_processed_dataset,
  SpaCyMorphAnalyzer,
)

df = pd.read_csv("full_data.csv", sep=";")
ds = DEvalDataset(df, text_column="text")

# Attach translations (must align with row order)
ds.add_translations("es", es_lines, "es")
ds.add_translations("fr", fr_lines, "fr")

# Build analyzers (loaded by you)
analyzers = {
  "es": SpaCyMorphAnalyzer("es_dep_news_trf"),
  "fr": SpaCyMorphAnalyzer("fr_dep_news_trf"),
}
for a in analyzers.values():
  a.load()

# Process for X subject and evaluate
processed = run_subject_pipeline(
  ds,
  analyzers=analyzers,
  source_column="text",
  subject_index_column="x_idx",
  output_prefix="x",
  languages=["es","fr"],
  article_offset=0,
  # If you run this from a notebook or a script without a __main__ guard,
  # set use_multiprocessing=False to avoid spawn errors.
  # use_multiprocessing=False,
)

metrics, metrics_df = evaluate_processed_dataset(
  processed,
  ["es","fr"],
  gold_gender_column="x_gender",
  output_prefix="x",
)
print(metrics_df)
```

## Notes
- SDK does not auto-load analyzers. Call `load()` on spaCy analyzers yourself.
- Accuracy-only metrics for now; extend in `analysis.py` later as needed.
- Multiprocessing: On macOS/Windows, ensure your script uses `if __name__ == "__main__":` when running in parallel.
  Alternatively, pass `use_multiprocessing=False` (and optionally `max_workers=1`) to run single-process safely.
