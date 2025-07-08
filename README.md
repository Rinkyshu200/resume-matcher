# 📄 Resume Matcher - AI-Powered Resume Analysis Tool

A **Streamlit** web app that uses **Natural Language Processing** (NLP) to match resumes with job descriptions. It supports single or batch analysis, identifies skill gaps, and provides visual insights to help job seekers and recruiters make informed decisions.

---

## 🚀 Features

* ✅ **Semantic Similarity** using TF-IDF + Cosine Similarity
* 📄 **Supports PDF & TXT** resumes
* 🧠 **Skill Extraction** using spaCy and pattern matching
* 📊 **Interactive Visualizations** with Plotly
* 📈 **Improvement Suggestions** for resume optimization
* 👥 **Bulk Resume Comparison** with ranking and breakdown

---

## 🛠 Tech Stack

| Component      | Technology            |
| -------------- | --------------------- |
| Frontend       | Streamlit             |
| Backend/NLP    | Python, spaCy         |
| ML & Vectors   | scikit-learn (TF-IDF) |
| PDF Processing | PyMuPDF               |
| Visualization  | Plotly                |

---

## 📁 Project Structure

```
resume-matcher/
├── app.py                          # Main app
├── utils/                          # Modular utilities
│   ├── text_extractor.py          # File parsing
│   ├── similarity_analyzer.py     # Matching logic
│   ├── skill_extractor.py         # Skill identification
│   ├── visualizations.py          # Charting
│   └── improvement_suggestions.py # Resume tips
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-matcher.git
cd resume-matcher
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate         # For Windows
# OR
source venv/bin/activate      # For macOS/Linux
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 🎯 How to Use

* **Single Resume Analysis**
  Upload a resume and job description → Click Analyze → Get similarity score, skill gaps, and visualizations.

* **Multi-Resume Comparison**
  Upload multiple resumes + job description → Click Compare → See ranking, individual reports, and matched skills.

---

## ❗ Troubleshooting

* **Missing spaCy Model**
  `python -m spacy download en_core_web_sm`

* **Port Conflict**
  `streamlit run app.py --server.port 8502`

---

## 📄 License

Licensed under [MIT License](LICENSE)

---

## 🙌 Acknowledgments

* [Streamlit](https://streamlit.io/)
* [spaCy](https://spacy.io/)
* [scikit-learn](https://scikit-learn.org/)
* [PyMuPDF](https://pymupdf.readthedocs.io/)

---

**Built with ❤️ for better hiring experiences**
[⭐ Star this repo](https://github.com/Rinkyshu200/resume-matcher)

---
