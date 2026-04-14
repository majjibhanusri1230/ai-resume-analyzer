from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text, extract_skills
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Resume Analyzer Backend Running!"

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    if not file.filename.endswith(('.pdf', '.doc', '.docx')):
        return jsonify({"error": "Invalid file format. Upload PDF/DOC/DOCX"}), 400

    try:
        text = extract_text(file)
        skills = extract_skills(text)

        skills = [skill.lower() for skill in skills]

        suggestions = []
        if "python" not in skills:
            suggestions.append("Add Python skill")
        if "react" not in skills:
            suggestions.append("Learn React")

        score = min(len(skills) * 15, 100)

        job_roles = {
            "Frontend Developer": ["html", "css", "javascript", "react"],
            "Backend Developer": ["python", "java", "sql"],
            "Full Stack Developer": ["python", "java", "html", "css", "javascript", "react"]
        }

        matched_roles = []
        for role, req_skills in job_roles.items():
            match_count = len(set(skills) & set(req_skills))
            if match_count >= 2:
                matched_roles.append(role)

        matched_roles = list(set(matched_roles))

        return jsonify({
            "skills": skills,
            "suggestions": suggestions,
            "score": score,
            "roles": matched_roles
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ FIXED PART (IMPORTANT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # dynamic port for Render
    app.run(host="0.0.0.0", port=port)