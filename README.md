## Contents

- [Contents](#contents)
- [DEval-MT - a Gender Bias Evaluation framework for German Machine Translation](#deval-mt---a-gender-bias-evaluation-framework-for-german-machine-translation)
  - [What is DEval-MT?](#what-is-deval-mt)
  - [Quickstart](#quickstart)
  - [Installation](#installation)
    - [0. create virtual environment (not necessary, but recommended)](#0-create-virtual-environment-not-necessary-but-recommended)
    - [1. install all dependencies](#1-install-all-dependencies)
    - [2. Download the spaCy models for whichever languages you need](#2-download-the-spacy-models-for-whichever-languages-you-need)
  - [Core components](#core-components)
- [Tools \& study](#tools--study)
  - [How to use the tools](#how-to-use-the-tools)
  - [How to reproduce the study](#how-to-reproduce-the-study)
- [Apis/methods/packages/platforms used](#apismethodspackagesplatforms-used)

## DEval-MT - a Gender Bias Evaluation framework for German Machine Translation

### What is DEval-MT?

DEval-MT is a Gender Bias Evaluation framework that provides a German Gender Bias Evaluation dataset and a pipeline to evaluate machine translation (MT) systems.

The pipeline automatically:

1. aligns source and target tokens using multilingual BERT (via `simalign`),
2. extracts the target-side phrase corresponding to the annotated source subject,
3. predicts the grammatical gender of that target phrase using pluggable morphological analyzers,
4. compares predictions against gold labels and provides analysis utilities.
5. generates plots for analysis results mentioned above.

---
### Quickstart
See [Installation](#installation) for the full setup

1. Install the package:
   ```bash
   pip install -e .
   ```
2. Download the spaCy model this example uses:
   ```bash
   python -m spacy download es_dep_news_trf
   ```
3. Run this minimal example — two rows straight out of `study/data/deval_dataset.csv` (source German, GPT-4o's actual Spanish translation):

```python
import pandas as pd
from deval_mt import DEvalDataset, run_subject_pipeline, evaluate_processed_dataset, SpaCyMorphAnalyzer

df = pd.DataFrame({
    "text":      ["Der Bauer geht gerne zur Arbeit.", "Die Bäuerin geht gerne zur Arbeit."],
    "x_idx":     [1, 1],              # index of the subject token ("Bauer"/"Bäuerin") in text.split()
    "adjective": ["none", "none"],    # "none" -> only the subject token + its article are extracted
    "x_gender":  ["MASCULINE", "FEMININE"],  # gold label
})

dataset = DEvalDataset(df, text_column="text")
dataset.add_translations("es", [
    "Al campesino le gusta ir a trabajar.",
    "A la campesina le gusta ir al trabajo.",
])

analyzer = SpaCyMorphAnalyzer("es_dep_news_trf")
analyzer.load()

dataset = run_subject_pipeline(
    dataset,
    analyzers={"es": analyzer},
    source_column="text",
    subject_index_column="x_idx",
)

results = evaluate_processed_dataset(dataset, gold_col="x_gender", predictor_col=None)
print(dataset.df[["x_phrase_es", "x_gender_es"]])
# 0   Al campesino    MASCULINE
# 1   la campesina    FEMININE
```

This aligns the German source to the Spanish translation, extracts the phrase aligned to `x_idx`, predicts its grammatical gender with spaCy, and scores it against `x_gender`.

For a fuller, runnable walkthrough — including the full plot suite (`plot_dir`), the logistic regression, and `ErrorAnalysis.grouped` for scoped comparisons — see [`deval_mt/usage_example.py`](deval_mt/usage_example.py).

---
### Installation

#### 0. create virtual environment (not necessary, but recommended)

#### 1. install all dependencies
``` bash
  pip install -e .
```

If you also want to fetch new translations (DeepL, GPT, SYSTRAN, Google, Microsoft), install the optional `translation` extra instead:
``` bash
  pip install -e ".[translation]"
```
This also requires API keys for whichever providers you use, set via a `.env` file in `tools/automized_translations/` — see [How to use the tools](#how-to-use-the-tools)
#### 2. Download the spaCy models for whichever languages you need
The study scripts use the following:
``` bash
  python -m spacy download es_dep_news_trf
  python -m spacy download fr_dep_news_trf
  python -m spacy download it_core_news_lg
  python -m spacy download ru_core_news_lg
  python -m spacy download uk_core_news_trf
```
---
### Core components

- `DEvalDataset` (`deval_mt/dataset.py`): wrapper around a pandas DataFrame.
  - stores source texts, translations and prediction columns,
  - allows adding translations via `add_translations`.

- `run_subject_pipeline` (`deval_mt/sdk.py`):
  - main function for processing a dataset
    - (re-)uses or creates word alignments,
    - computes source subject phrase indices,
    - extracts aligned target phrases per language,
    - runs morphological analyzers to predict gender,
    - writes results into new columns like `x_phrase_es`, `x_gender_es`, etc.

- `evaluate_processed_dataset` (`deval_mt/sdk.py`):
  - basic evaluation of a processed dataset
    - runs `ErrorAnalysis`, `ConfusionMatrix`, and (optionally) `LogisticRegressionAnalysis`,
    - optional `plot_dir`/`output_dir` to render plots / save CSVs.
    - single scope only, no built-in grouping -- for multiple scopes (e.g. one call per sentence style) or a grouped comparison within one call, use `ErrorAnalysis.grouped` directly instead (see `analysis/` below), like `study/usage_example_process_data.py` does.

- `run_full_pipeline` (`deval_mt/sdk.py`): `run_subject_pipeline` + `evaluate_processed_dataset` in one call.

- `alignment/`:
  - `AlignmentProcessor`: computes word alignments between source and translations.
  - `WordAlignment`: helper to query and serialize alignments.

- `morphological_analysis/`:
  - `Gender`: enum with MASCULINE, FEMININE, NEUTER, DIVERSE, UNKNOWN.
  - `BaseMorphologicalAnalyzer`: abstract interface.
  - `SpaCyMorphAnalyzer`: spaCy-based implementation (uses language-specific models).
  - `HebrewMorphAnalyzer`: uses spaCy's Hebrew tokenizer + a word-ending heuristic
  - `QalsadiMorphAnalyzer`: qalsadi-based implementation, for Arabic.

- `analysis/`:
  - `ErrorAnalysis`: accuracy + detailed error types, `ErrorAnalysis.grouped`: runs `ErrorAnalysis` once per value of a column, for scoped comparisons (e.g. accuracy for masculine-gold rows vs. feminine-gold rows).
  - `ConfusionMatrix`: confusion matrices & precision/recall/F1 per gender.
  - `LogisticRegressionAnalysis`: relates predictors (e.g. stereotypicality) to correctness.
  - above three support an optional filter column, to scope analysis to a subset (e.g. one sentence style).
  - `test_direction_skew`, `test_group_gap`, `test_paired_gap` (`significance.py`) (binomial / chi-square / McNemar) for different comparison shapes.
  - `compare_accuracy_by_language` (`style_comparison.py`): diffs accuracy between two conditions, per model and per language.
  - `plotting.py`: renders any of the above as a figure (error-type heatmap, gold→predicted Sankey flow, stereotypicality curve, accuracy heatmap, significance-star tables), plus `save_dataframes` to write results to CSV.

This modular design makes it easy to plug in:
- new languages,
- different morphological analyzers,
- additional analysis modules.

## Tools & study

- `tools/automized_translations/`: automatic translation fetching for multiple MT systems.
- `tools/create_deval_synth/`: dataset generation and extension.
- `study/`: study results and analysis scripts (the dataset itself, its translations, and an analysis pipeline that reproduces the paper's figures/tables).

### How to use the tools

- `tools/create_deval_synth/`: generates a dataset from templates.
  - run from within its own directory:
    ```bash
    cd tools/create_deval_synth
    python main.py
    ```
  - reads `dataset.csv` (hand-authored sentence templates, placeholders like `<x_nom_sg>`), `groups.py` (occupation nouns, declined per gender), `names.py` (first names), `adjectives.py` (currently just `trans`),
  - writes generated sentences to `output.csv` (not committed, regenerate as needed).
  - to add a template: add a row to `dataset.csv`. to add a demographic axis: add an entry to `adjectives.py` (already supports a second axis, e.g. nationality, just not activated for this study).
  - schema `DEvalDataset`/`run_subject_pipeline` expect, whether from `output.csv` or a hand-built DataFrame:
    - a source text column (e.g. `text`),
    - one or more `<subject>_idx` integer columns (position of the subject within sentence)
    - an `adjective` column (`"none"` = article + noun only, any other value = adjective precedes the noun),
    - a gold gender column per subject, one of `MASCULINE`/`FEMININE`/`DIVERSE`,
    - optionally a `<subject>_stereotypical` column (0/1), for `LogisticRegressionAnalysis`/`predictor_col`,
    - translations attached separately via `add_translations`, not part of the CSV schema.

- `tools/automized_translations/`: fetches translations from DeepL, GPT, SYSTRAN, Google, Microsoft.
  - requires API keys in a `.env` file:
    ```
    DEEPL_API_KEY=...
    OPENAI_API_KEY=...
    MICROSOFT_TRANSLATOR_KEY=...
    SYSTRAN_API_URL=...
    SYSTRAN_API_KEY=...
    GOOGLE_CLOUD_PROJECT=...
    GOOGLE_APPLICATION_CREDENTIALS=./your-service-account.json
    ```
  - `dataset_translation.py`: ready-to-edit example covering many languages/providers at once.
  - `retranslate_errors.py`: re-attempts only the failed lines (marked `ERROR:`), without re-translating everything.

### How to reproduce the study

Run these in order, from the repository root:

```bash
python study/usage_example_generate_processed_data.py
```
Builds `study/processed_data/<model>_processed.csv` for every model, from `study/data/deval_dataset.csv` + `study/data/translations/`, via `run_subject_pipeline` (see [Core components](#core-components)). Skips a model whose output already exists.

```bash
python study/usage_example_process_data.py
```
Reads the generated files and analyzes them using a more comprehensive approach than just basic evaluation via `evaluate_processed_dataset`, writing per-model results to `study/outputs/<model>/`, then aggregating across models into `study/outputs/summary/`.


## Apis/methods/packages/platforms used
- Word alignment: [Simalign](https://github.com/cisnlp/simalign)
- Morphological analysis models:
  - [spaCy](https://spacy.io/)
  - [Qalsadi](https://github.com/linuxscout/qalsadi)
- Automized translations:
  - [DeepL](https://api.deepl.com)
  - [Google](https://cloud.google.com/translate)
  - [GPT](https://api.openai.com/v1/chat/completions)
  - [Microsoft](https://api.cognitive.microsofttranslator.com)
  - [Systran](https://www.systransoft.com/translation-products/translate-api/)
