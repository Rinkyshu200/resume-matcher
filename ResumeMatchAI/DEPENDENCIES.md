# Dependencies for Resume Matcher

## Core Dependencies

### Web Framework
- **streamlit>=1.46.1** - Main web application framework

### Data Processing
- **pandas>=2.3.0** - Data manipulation and analysis
- **numpy>=2.3.1** - Numerical computing

### Machine Learning & NLP
- **scikit-learn>=1.7.0** - TF-IDF vectorization and similarity analysis
- **spacy>=3.8.7** - Natural language processing and skill extraction

### File Processing
- **PyMuPDF>=1.26.3** - PDF text extraction (imported as `fitz`)

### Visualization
- **plotly>=6.2.0** - Interactive charts and graphs

## Installation Commands

### Using pip:
```bash
pip install streamlit pandas numpy scikit-learn spacy pymupdf plotly
```

### Using uv (alternative):
```bash
uv add streamlit pandas numpy scikit-learn spacy pymupdf plotly
```

### spaCy Language Model:
```bash
python -m spacy download en_core_web_sm
```

## Package Purposes

| Package | Purpose | Used In |
|---------|---------|---------|
| streamlit | Web interface and UI components | app.py |
| pandas | Data frames for multi-resume comparison | app.py, visualizations.py |
| numpy | Numerical operations for similarity | similarity_analyzer.py |
| scikit-learn | TF-IDF vectorization and cosine similarity | similarity_analyzer.py |
| spacy | NLP processing and skill extraction | skill_extractor.py |
| pymupdf | PDF text extraction | text_extractor.py |
| plotly | Interactive visualizations | visualizations.py |

## Alternative Packages (if issues occur)

If sentence-transformers installation fails:
- The app uses scikit-learn's TF-IDF as the primary similarity method
- sentence-transformers was replaced with TF-IDF for compatibility

## System Requirements

- Python 3.11+
- 2GB+ RAM (4GB recommended)
- Multi-core CPU (recommended for batch processing)