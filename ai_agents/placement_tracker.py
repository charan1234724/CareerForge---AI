from ai_agents.ats_checker import calculate_ats_score
from ai_agents.resume_improver import analyze_resume_improvement


from ai_agents.score_engine import calculate_resume_scores


def calculate_readiness(
    resume,
    applications_count,
    interview_completed=False
):

    # -----------------------------
    # Get all scores from ONE engine
    # -----------------------------

    scores = calculate_resume_scores(
        resume
    )

    ats_score = scores.ats_score

    resume_score = scores.resume_score

    # -----------------------------
    # Applications Score
    # -----------------------------

    application_score = min(
        applications_count * 5,
        100
    )

    # -----------------------------
    # Interview Score
    # -----------------------------

    interview_score = (
        100 if interview_completed else 50
    )

    # -----------------------------
    # Overall Readiness
    # -----------------------------

    readiness = round(

        ats_score * 0.30 +

        resume_score * 0.30 +

        application_score * 0.20 +

        interview_score * 0.20

    )

    # -----------------------------
    # Recommendations
    # -----------------------------

    recommendations = []

    if ats_score < 80:

        recommendations.append(

            "Improve ATS keywords in your resume."

        )

    if resume_score < 80:

        recommendations.append(

            "Improve your resume quality and projects."

        )

    if application_score < 60:

        recommendations.append(

            "Apply for more jobs every week."

        )

    if interview_score < 80:

        recommendations.append(

            "Practice mock interviews."

        )

    if not recommendations:

        recommendations.append(

            "Excellent! Keep maintaining your profile."

        )

    # -----------------------------
    # Return
    # -----------------------------

    return {

        "score": readiness,

        "ats": ats_score,

        "resume": resume_score,

        "applications": application_score,

        "interview": interview_score,

        "recommendations": recommendations

    }