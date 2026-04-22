import pdfplumber
from docx import Document

def extract_text(file):
    # text = ""
    # with pdfplumber.open(file) as pdf:
    #     for page in pdf.pages:
    #         if page.extract_text():
    #             text += page.extract_text()
    # return text

    
    if file.filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.filename.endswith(".docx"):
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        return ""


def extract_skills(text):
    skills_list = ["python", "java", "html", "css", "javascript", "sql", "react"]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))