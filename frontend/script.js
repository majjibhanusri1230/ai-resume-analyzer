async function uploadResume() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a resume!");
        return;
    }

    document.getElementById("loading").style.display = "block";

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("loading").style.display = "none";

        // ⭐ Score
        document.getElementById("score").innerText = data.score + " / 100";

        // 📊 Progress Bar
        document.getElementById("progress").style.width = data.score + "%";

        // ✅ Skills
        let skillsHTML = "";
        data.skills.forEach(skill => {
            skillsHTML += `<span class="skill">${skill}</span>`;
        });
        document.getElementById("skills").innerHTML = skillsHTML;

        // 🎯 Roles
        document.getElementById("roles").innerText =
            data.roles.length > 0
            ? data.roles.join(", ")
            : "No matching roles yet";

        // 💡 Suggestions
        document.getElementById("suggestions").innerText =
            data.suggestions.length > 0
            ? data.suggestions.join(", ")
            : "Great job! Your resume looks strong 💪";

        // 🔥 Confidence Message
        let msg = "";
        if (data.score >= 80) {
            msg = "🔥 Excellent! You're job-ready!";
        } else if (data.score >= 50) {
            msg = "💪 Good! Keep improving!";
        } else {
            msg = "🚀 Don't worry! Keep learning and growing!";
        }

        document.getElementById("confidence").innerText = msg;

    } catch (error) {
        document.getElementById("loading").style.display = "none";
        alert("Error connecting to backend");
    }
}