# DEval-MT (SDK only)
Python SDK to evaluate gender in MT outputs using alignment + morphological analyzers.

## Install
```bash
# install in editable mode, since this is a dev repo and not yet available in package managers
pip install -e .

# Optionally download required SpaCy models if you plan to use SpaCy analyzers
python -m spacy download es_dep_news_trf
python -m spacy download fr_dep_news_trf
# ... add more as needed
```

## Usage
A full usage example can be found in `usage_example.py`.