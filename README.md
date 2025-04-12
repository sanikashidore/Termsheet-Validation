# 📄 Term Sheet Validator

A web-based application to analyze, validate, and summarize legal term sheets — including support for scanned documents using OCR.

## 🔍 Features

- ✅ Validate uploaded legal documents (PDF, DOCX, TXT, scanned images)
- 📌 Extract key details: parties, dates, financial & legal terms
- 📝 Generate clear bullet-point summaries
- ⚠️ Highlight errors and warnings based on validation rules
- 🧾 Download results as JSON
- 📊 Display template compliance score visually
- 🧠 Simple extractive summarization using regex-based heuristics

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, Jinja2
- **Parsing & NLP:** Regex, EasyOCR
- **Document Support:** PyMuPDF (PDF), python-docx (DOCX), plain text

## 🚀 How It Works

1. User uploads a term sheet file (PDF, TXT, DOCX, or image).
2. OCR is applied (if needed) to extract raw text.
3. Key entities and sections are identified and extracted.
4. Summary and validation results are generated.
5. Output is displayed in a clean UI and available for download.

## 🖼 Demo

Link: https://drive.google.com/file/d/1xWDSka5GrpC15M7e5kzE-ivIP-VdRh5_/view?usp=sharing

## 🛠 Run Locally

```bash
git clone https://github.com/your-username/term-sheet-validator.git
cd term-sheet-validator
pip install -r requirements.txt
python app.py
