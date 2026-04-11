import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_skills(text):
    skills_list = ["python", "java", "html", "css", "javascript", "sql", "react"]
    found_skills = []

    for word in text.lower().split():
        if word in skills_list:
            found_skills.append(word)

    return list(set(found_skills))