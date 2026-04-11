from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text, extract_skills

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

    try:
        text = extract_text(file)
        skills = extract_skills(text)

        # Suggestions
        suggestions = []
        if "python" not in skills:
            suggestions.append("Add Python skill")
        if "react" not in skills:
            suggestions.append("Learn React")

        # ⭐ Resume Score
        score = len(skills) * 20
        if score > 100:
            score = 100

        # 🎯 Job Role Matching
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

        return jsonify({
            "skills": skills,
            "suggestions": suggestions,
            "score": score,
            "roles": matched_roles
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)