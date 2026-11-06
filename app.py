import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from backend.services.resume_reader import (
    read_resume
)

from backend.services.catalog_service import (
    get_module_by_title
)

from backend.services.cosmos_service import (
    get_profile,
    save_profile,
    get_assessment,
    save_assessment,
    get_learning_path,
    get_learning_progress,
    get_evaluation,
    get_certificate,
    save_assessment_result,
    get_assessment_result
)
from backend.agents.profile_agent import (
    generate_profile
)

from backend.agents.assessment_agent import (
    generate_assessment
)

from backend.agents.tutor_agent import (
    answer_question
)

from backend.agents.planner_agent import (
    generate_learning_path
)

app = Flask(__name__)

app.secret_key = "adaptive-learning-secret-key"

UPLOAD_FOLDER = "data/resumes"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================
# Dashboard
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        user_id=session.get(
            "userId"
        )
    )


# ==========================================
# Resume Upload
# ==========================================

@app.route(
    "/upload-resume",
    methods=["GET", "POST"]
)
def upload_resume():

    if request.method == "POST":

        try:

            uploaded_file = request.files.get(
                "resume"
            )

            if not uploaded_file:

                return render_template(
                    "upload_resume.html",
                    error="Please select a PDF file."
                )

            if uploaded_file.filename == "":

                return render_template(
                    "upload_resume.html",
                    error="No file selected."
                )

            if not uploaded_file.filename.lower().endswith(
                ".pdf"
            ):

                return render_template(
                    "upload_resume.html",
                    error="Only PDF files are supported."
                )

            file_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.filename
            )

            uploaded_file.save(
                file_path
            )

            # ==================================
            # Extract Resume
            # ==================================

            resume_text = read_resume(
                file_path
            )

            # ==================================
            # Generate Profile
            # ==================================

            profile = generate_profile(
                resume_text
            )

            user_id = str(
                uuid.uuid4()
            )

            profile["id"] = user_id
            profile["userId"] = user_id

            save_profile(
                profile
            )

            # ==================================
            # Generate Assessment
            # ==================================

            assessment = generate_assessment(
                profile
            )

            assessment["id"] = str(
                uuid.uuid4()
            )

            assessment["userId"] = user_id

            save_assessment(
                assessment
            )

            # ==================================
            # Store Session
            # ==================================

            session["userId"] = user_id

            # ==================================
            # Redirect to Profile Page
            # ==================================

            return redirect(
                url_for(
                    "profile"
                )
            )

        except Exception as ex:

            return render_template(
                "upload_resume.html",
                error=str(ex)
            )

    return render_template(
        "upload_resume.html"
    )


# ==========================================
# Profile
# ==========================================

@app.route("/profile")
def profile():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    profile_data = get_profile(
        user_id
    )

    return render_template(
        "profile.html",
        profile=profile_data
    )


# ==========================================
# Assessment
# ==========================================

@app.route("/assessment")
def assessment():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    assessment_data = get_assessment(
        user_id
    )

    return render_template(
        "assessment.html",
        assessment=assessment_data
    )


# ==========================================
# Submit Assessment
# ==========================================

@app.route(
    "/submit-assessment",
    methods=["POST"]
)
def submit_assessment():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    assessment_data = get_assessment(
        user_id
    )

    questions = assessment_data["assessment"]

    score = 0

    total_questions = len(
        questions
    )

    results = []

    skill_gaps = []

    for index, question in enumerate(
        questions,
        start=1
    ):

        selected_answer = request.form.get(
            f"q{index}"
        )

        correct_answer = question["answer"]

        is_correct = (
            selected_answer ==
            correct_answer
        )

        if is_correct:

            score += 1

        else:

            skill_gaps.append(
                question.get(
                    "skill",
                    "General"
                )
            )

        results.append({

            "question":
                question["question"],

            "selected":
                selected_answer,

            "correct":
                correct_answer,

            "isCorrect":
                is_correct,

            "skill":
                question.get(
                    "skill",
                    "General"
                )

        })

    percentage = round(
        (
            score /
            total_questions
        ) * 100
    )

    learner_level = (
        "Intermediate"
        if percentage >= 70
        else "Beginner"
    )

    assessment_result = {

        "id": str(
            uuid.uuid4()
        ),

        "userId": user_id,

        "score": percentage,

        "totalQuestions":
            total_questions,

        "correctAnswers":
            score,

        "learnerLevel":
            learner_level,

        "skillGaps":
            list(
                set(
                    skill_gaps
                )
            ),

        "results":
            results
    }

    save_assessment_result(
        assessment_result
    )

    return redirect(
        url_for(
            "assessment_result"
        )
    )
# ==========================================
# Assessment Result
# ==========================================

@app.route(
    "/assessment-result"
)
def assessment_result():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    result = get_assessment_result(
        user_id
    )

    if not result:

        return redirect(
            url_for(
                "assessment"
            )
        )

    return render_template(
        "assessment_result.html",
        result=result
    )
# ==========================================
# Learning Path
# ==========================================

@app.route(
    "/learning-path"
)
def learning_path():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    profile = get_profile(
        user_id
    )

    assessment_result = (
        get_assessment_result(
            user_id
        )
    )

    if not assessment_result:

        return redirect(
            url_for(
                "assessment"
            )
        )

    learning_path_data = (
        generate_learning_path(
            profile,
            assessment_result
        )
    )

    return render_template(
        "learning_path.html",
        learning_path=learning_path_data
    )

# ==========================================
# Tutor
# ==========================================

@app.route(
    "/tutor",
    methods=["GET", "POST"]
)
def tutor():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    answer = ""

    if request.method == "POST":

        question = request.form.get(
            "question"
        )

        profile_data = get_profile(
            user_id
        )

        path = get_learning_path(
            user_id
        )

        if not path:

            answer = (
                "Learning Path not available."
            )

        else:

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
# Progress
# ==========================================

@app.route("/progress")
def progress():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    progress_data = get_learning_progress(
        user_id
    )

    return render_template(
        "progress.html",
        progress=progress_data
    )


# ==========================================
# Evaluation
# ==========================================

@app.route("/evaluation")
def evaluation():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    evaluation_data = get_evaluation(
        user_id
    )

    return render_template(
        "evaluation.html",
        evaluation=evaluation_data
    )


# ==========================================
# Certificate
# ==========================================

@app.route("/certificate")
def certificate():

    user_id = session.get(
        "userId"
    )

    if not user_id:

        return redirect(
            url_for(
                "upload_resume"
            )
        )

    certificate_data = get_certificate(
        user_id
    )

    return render_template(
        "certificate.html",
        certificate=certificate_data
    )


# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for(
            "upload_resume"
        )
    )


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )