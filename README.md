## What is DEval-MT?

DEval-MT is a small Python SDK to evaluate **gender marking in machine translation outputs**.
It is designed for datasets where:

- you have source sentences (e.g. German),
- one or more machine-translated target sentences (e.g. Spanish, French),
- annotated subject positions in the source (e.g. `x_idx`),
- and gold gender labels for these subjects (e.g. `x_gender`).

The pipeline automatically:

1. aligns source and target tokens using multilingual BERT (via `simalign`),
2. extracts the target-side phrase corresponding to the annotated source subject,
3. predicts the grammatical gender of that target phrase using pluggable morphological analyzers,
4. compares predictions against gold labels and provides analysis utilities.
5. **(NEW)** generates plots for analysis results mentioned above.
6. **(NEW)** automatically translates the source sentences in dataset with multiple MT models: DeepL, ChatGPT, SYSTRAN, Google, Microsoft. (for chatgpt now it is gpt-4o/gpt-4o-mini)

## Core components

- `DEvalDataset` (`Dataset.py`): wrapper around a pandas DataFrame.
  - stores source texts, translations and prediction columns,
  - allows adding translations (manually or via a custom translation function).

- `run_subject_pipeline` (`sdk.py`):
  - main high-level function:
    - (re-)uses or creates word alignments,
    - computes source subject phrase indices,
    - extracts aligned target phrases per language,
    - runs morphological analyzers to predict gender,
    - writes results into new columns like `x_phrase_es`, `x_gender_es`, etc.

- `alignment/`:
  - `AlignmentProcessor`: computes word alignments between source and translations.
  - `WordAlignment`: helper to query and serialize alignments.

- `morphological_analysis/`:
  - `BaseMorphologicalAnalyzer`: abstract interface.
  - `SpaCyMorphAnalyzer`: spaCy-based implementation (uses language-specific models).
  - `Gender`: enum with MASCULINE, FEMININE, NEUTER, DIVERSE, UNKNOWN.

- `analysis/`:
  - `ErrorAnalysis`: accuracy + detailed error types.
  - `ConfusionMatrix`: confusion matrices & precision/recall/F1 per gender.
  - `LogisticRegressionAnalysis`: relates predictors (e.g. stereotypicality) to correctness.

- **(NEW)**`automized_translations/`:
  - `systran_translate.py`, `gpt_translate.py`, `deepl_translate.py`, `google_translate.py`, `microsoft_translate.py`: translates sentences with multiple models.
  - `list_translator.py`: integrates different translation models and languages, multiple inputs possible 
  - use `test_list_translator.py` to test/try the translation functions
  - use `dataset_translation.py` to translate a proper dataset

This modular design makes it easy to plug in:
- new languages,
- different morphological analyzers,
- additional analysis modules,
- different translation models.

## Installation Linux

### 0. create virtual environment: (not necessary, but recommendet)
    ``` bash
	Linux: 
		sudo apt install python3-venv
		python3 -m venv <name of venv>
		source <name of venv>/bin/activate
    ```
### 1. install all dependencies
    ``` bash
	Linux:
		pip install -e .
    ```
	
### 2. If you want to use the usage_example.py download the SpaCy analyzers
    ``` bash
	Linux: python -m spacy download es_dep_news_trf
	       python -m spacy download fr_dep_news_trf
    ```

## Installation Windows (currently needs python version < 3.12)
- On Windows, you may need to use a version manager such as **pyenv for Windows** or **pyenv-win** to install and switch between Python versions.  
  - ~~**TODO:** Add a reference or setup guide for `pyenv-win` to this README.~~
  - [`pyenv-win`](https://github.com/pyenv-win/pyenv-win)
  - **(TBC)** All known working Python versions: 3.11
- Other than that the installation steps are the same as in the Linux Installation

## Usage
A full, runnable example can be found in [`usage_example.py`, `usage_example_2.py`].

## Apis/methods/packages/platforms used
- Word alignment: [Simalign](https://github.com/cisnlp/simalign)
- A platform hosting models: [Huggingface](https://huggingface.co/)
- Morphological analysis model: [spaCy](https://spacy.io/)