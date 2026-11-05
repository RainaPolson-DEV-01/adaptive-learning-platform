from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from backend.services.cosmos_service import (
    get_profile,
    get_learning_path,
    get_learning_progress,
    get_evaluation,
    get_certificate,
    save_profile
)

from backend.services.catalog_service import (
    get_module_by_title
)

from backend.services.resume_reader import (
    read_resume
)

from backend.agents.profile_agent import (
    generate_profile
)

from backend.agents.tutor_agent import (
    answer_question
)

app = Flask(__name__)


# ==========================================
# Dashboard
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# Resume Upload Page
# ==========================================

@app.route(
    "/upload-resume",
    methods=["GET", "POST"]
)
def upload_resume():

    if request.method == "POST":

        uploaded_file = request.files.get(
            "resume"
        )

        if uploaded_file:

            file_path = (
                f"data/resumes/"
                f"{uploaded_file.filename}"
            )

            uploaded_file.save(
                file_path
            )

            resume_text = read_resume(
                file_path
            )

            profile = generate_profile(
                resume_text
            )

            profile["id"] = "1001"
            profile["userId"] = "1001"

            save_profile(
                profile
            )

            return redirect(
                url_for(
                    "profile"
                )
            )

    return render_template(
        "upload_resume.html"
    )


# ==========================================
# Profile Page
# ==========================================

@app.route("/profile")
def profile():

    profile_data = get_profile(
        "1001"
    )

    return render_template(
        "profile.html",
        profile=profile_data
    )


# ==========================================
# Learning Path Page
# ==========================================

@app.route("/learning-path")
def learning_path():

    path = get_learning_path(
        "1001"
    )

    return render_template(
        "learning_path.html",
        path=path
    )


# ==========================================
# AI Tutor Page
# ==========================================

@app.route(
    "/tutor",
    methods=["GET", "POST"]
)
def tutor():

    answer = ""

    if request.method == "POST":

        question = request.form.get(
            "question"
        )

        profile_data = get_profile(
            "1001"
        )

        path = get_learning_path(
            "1001"
        )

        current_module = (
            path["modules"][0]
        )

        module = get_module_by_title(
            current_module["title"]
        )

        answer = answer_question(
            profile_data,
            module,
            question
        )

    return render_template(
        "tutor.html",
        answer=answer
    )


# ==========================================
# Progress Page
# ==========================================

@app.route("/progress")
def progress():

    progress_data = get_learning_progress(
        "1001"
    )

    return render_template(
        "progress.html",
        progress=progress_data
    )


# ==========================================
# Evaluation Page
# ==========================================

@app.route("/evaluation")
def evaluation():

    evaluation_data = get_evaluation(
        "1001"
    )

    return render_template(
        "evaluation.html",
        evaluation=evaluation_data
    )


# ==========================================
# Certificate Page
# ==========================================

@app.route("/certificate")
def certificate():

    certificate_data = get_certificate(
        "1001"
    )

    return render_template(
        "certificate.html",
        certificate=certificate_data
    )


# ==========================================
# Application Entry
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )