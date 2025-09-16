# Gender Bias Evaluation Pipeline - Setup Guide

## Overview
This pipeline allows you to evaluate gender bias in machine translation models by comparing the gender of translated words against the original gender annotations in our dataset.

## Installation

### 1. Basic Requirements
```bash
pip install -r requirements.txt
```

### 2. Language-Specific Models

#### SpaCy Models (Required for most languages)
```bash
# Spanish (high accuracy transformer model - recommended)
python -m spacy download es_dep_news_trf

# French (high accuracy transformer model - recommended)  
python -m spacy download fr_dep_news_trf

# German (high accuracy transformer model - recommended)
python -m spacy download de_dep_news_trf

# Other languages (smaller models for faster processing)
python -m spacy download en_core_web_sm
python -m spacy download it_core_news_sm
python -m spacy download pt_core_news_sm
python -m spacy download ru_core_news_sm
```

#### Arabic Support (Optional)
```bash
pip install qalsadi pyarabic
```

#### Hebrew Support (Optional)
```bash
pip install hebrew_tokenizer
```

### 3. Verification
Run the setup verification script:
```bash
python verify_setup.py
```

## Quick Start

### Step 1: Get sentences to translate
```python
from pipeline import GenderBiasEvaluationPipeline

# Initialize pipeline with your dataset
pipeline = GenderBiasEvaluationPipeline("data_huge.csv")

# Get clean sentences (without annotations)
sentences = pipeline.get_source_sentences()

# Save for translation
with open("sentences_to_translate.txt", "w", encoding="utf-8") as f:
    for sentence in sentences:
        f.write(sentence + "\n")
```

### Step 2: Translate the sentences
Translate the sentences using your MT model/system into your target language(s).

### Step 3: Evaluate your translations
```python
# Load your translations
spanish_translations = []  # Your Spanish translations here
french_translations = []   # Your French translations here

# Run evaluation
results = pipeline.evaluate_translations({
    'es': spanish_translations,
    'fr': french_translations
})

# Generate report
report = pipeline.generate_report(results, "my_evaluation_report.txt")
print(report)
```

## Supported Languages

### Fully Supported (with spaCy)
- Spanish (es) - ✅ High accuracy with transformer models
- French (fr) - ✅ High accuracy with transformer models  
- German (de) - ✅ High accuracy with transformer models
- English (en) - ✅ 
- Italian (it) - ✅
- Portuguese (pt) - ✅
- Russian (ru) - ✅

### Experimental Support
- Arabic (ar) - ⚠️ Requires additional libraries
- Hebrew (he) - ⚠️ Requires additional libraries

### Adding New Languages
To add support for a new language:

1. **If spaCy model exists**: Update `SpaCyAnalyzer.MODEL_MAP` in `morphological_analysis/spacy_analyzer.py`
2. **If custom analyzer needed**: Create new analyzer class inheriting from `BaseMorphologicalAnalyzer`
3. **Update factory**: Add language mapping in `AnalyzerFactory.LANGUAGE_ANALYZER_MAP`

## Advanced Usage

### Custom Alignment Parameters
```python
pipeline = GenderBiasEvaluationPipeline(
    "data_huge.csv",
    alignment_model="bert",      # or "xlm-roberta"
    alignment_token_type="bpe",  # or "word"
    alignment_method="itermax"   # currently the only supported method
)
```

### Progress Monitoring
```python
def my_progress_callback(message: str):
    print(f"[{datetime.now()}] {message}")

results = pipeline.evaluate_translations(
    translations,
    progress_callback=my_progress_callback
)
```

## Troubleshooting

### Common Issues

1. **"Language not supported" error**
   - Install the required spaCy model for your language
   - Check available languages: `pipeline.get_available_languages()`

2. **"Dataset missing required columns" error**
   - Ensure your dataset has columns: text, x_gender, y_gender, x_idx, y_idx
   - Check the dataset format matches the expected structure

3. **Memory issues with large datasets**
   - Use smaller batch sizes in alignment processing
   - Consider processing languages one at a time

4. **Alignment accuracy issues**
    - Try different alignment models (bert, xlm-roberta)
    - Experiment with different token types (bpe, word)
    - (Method is fixed to itermax for stability)
    - Check if sentences are too long or complex

### Getting Help

1. Check the example usage: `python example_usage.py`
2. Run setup verification: `python verify_setup.py` 
3. Review the generated reports for insights into model performance

## Citation

If you use this pipeline in your research, please cite:
```bibtex
@software{gender_bias_eval_2024,
  title={Gender Bias Evaluation Pipeline for Machine Translation},
  author={Your Name},
  year={2024},
  url={https://github.com/your-repo}
}
```
