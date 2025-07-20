# parser.py
import pdfplumber
import spacy
import os

# Load the small English model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_details(text):
    doc = nlp(text)
    details = {"name": "", "skills": [], "education": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not details["name"]:
            details["name"] = ent.text
        elif ent.label_ == "ORG":
            details["education"].append(ent.text)
    return details

if __name__ == "__main__":
    sample_pdf = "sample_resume.pdf"  # Make sure this file exists in the same folder
    try:
        extracted_text = extract_text_from_pdf(sample_pdf)
        result = extract_details(extracted_text)
        print("=== Extracted Resume Details ===")
        print("Name:", result["name"])
        print("Education:", ", ".join(result["education"]))
        print("Skills:", ", ".join(result["skills"]) if result["skills"] else "Not detected")
    except Exception as e:
        print("Error:", str(e))
