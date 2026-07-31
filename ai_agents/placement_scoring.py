from ai_agents.resume_improver import analyze_resume_improvement


def calculate_placement_scores(resume_text):

    analysis = analyze_resume_improvement(resume_text)

    resume_score = analysis["score"]

    strengths = len(analysis["strengths"])

    weaknesses = len(analysis["weaknesses"])

    projects = len(analysis["projects"])

    certifications = len(analysis["certifications"])

    career = (
        analysis["career_paths"][0]
        if analysis["career_paths"]
        else "General Software Engineer"
    )

    hiring_probability = min(
        100,
        resume_score + 10
    )

    interview_score = min(
        100,
        60 + strengths * 5
    )

    company_readiness = min(
        100,
        55 + projects * 8
    )

    if resume_score >= 85:
        salary = "12-18 LPA"

    elif resume_score >= 70:
        salary = "8-12 LPA"

    elif resume_score >= 60:
        salary = "5-8 LPA"

    else:
        salary = "3-5 LPA"

    return {

        "placement_score": resume_score,

        "hiring_probability": hiring_probability,

        "interview_score": interview_score,

        "company_readiness": company_readiness,

        "salary": salary,

        "career": career,

        "strengths": analysis["strengths"],

        "weaknesses": analysis["weaknesses"],

        "projects": analysis["projects"],

        "certifications": analysis["certifications"]

    }