from .career_paths import CAREER_PATHS
from .career_roadmap import (
    generate_roadmap
)


def detect_career_paths(text):

    matches = []

    for role, data in CAREER_PATHS.items():

        count = 0

        for skill in data["skills"]:

            if skill.lower() in text:
                count += 1

        if count > 0:

            matches.append(
                (
                    role,
                    count
                )
            )

    matches.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        role
        for role, score in matches[:3]
    ]


def analyze_resume_improvement(
    resume_text
):

    text = resume_text.lower()

    score = 0

    strengths = []
    weaknesses = []

    # -------------------------
    # Core Skills Detection
    # -------------------------

    if "python" in text:
        score += 15
        strengths.append("Python")

    if "django" in text:
        score += 15
        strengths.append("Django")

    if "react" in text:
        score += 10
        strengths.append("React")

    if "mysql" in text:
        score += 10
        strengths.append("MySQL")

    if "javascript" in text:
        score += 5
        strengths.append("JavaScript")

    if "html" in text:
        score += 5
        strengths.append("HTML")

    if "css" in text:
        score += 5
        strengths.append("CSS")

    if "machine learning" in text:
        score += 10
        strengths.append("Machine Learning")

    if "ai" in text:
        score += 10
        strengths.append("Artificial Intelligence")

    if "github" in text:
        score += 5
        strengths.append("GitHub")

    # -------------------------
    # Projects
    # -------------------------

    if "project" in text:
        score += 15
        strengths.append(
            "Multiple Projects"
        )

    # -------------------------
    # Internship
    # -------------------------

    if "intern" in text:
        score += 15
        strengths.append(
            "Internship Experience"
        )

    # -------------------------
    # Missing Skills
    # -------------------------

    if "docker" not in text:
        weaknesses.append("Docker")
    else:
        score += 5

    if "aws" not in text:
        weaknesses.append("AWS")
    else:
        score += 5

    if "rest api" not in text:
        weaknesses.append(
            "REST API"
        )
    else:
        score += 5

    if "git" not in text:
        weaknesses.append("Git")
    else:
        score += 5

    if "postgresql" not in text:
        weaknesses.append(
            "PostgreSQL"
        )

    if "kubernetes" not in text:
        weaknesses.append(
            "Kubernetes"
        )

    # -------------------------
    # Career Path Detection
    # -------------------------

    career_paths = detect_career_paths(
        text
    )

    projects = []

    certifications = []

    for role in career_paths:

        projects.extend(
            CAREER_PATHS[role]["projects"]
        )

        certifications.extend(
            CAREER_PATHS[role]["certifications"]
        )

    # Remove duplicates

    projects = list(
    dict.fromkeys(projects)
)[:5]
    
    certifications = list(
    dict.fromkeys(certifications)
)[:5]

    # -------------------------
    # Improvement Suggestions
    # -------------------------

    suggestions = []

    if "docker" not in text:
        suggestions.append(
            "Learn Docker and containerization."
        )

    if "aws" not in text:
        suggestions.append(
            "Learn AWS cloud fundamentals."
        )

    if "rest api" not in text:
        suggestions.append(
            "Build a Django REST API project."
        )

    if "postgresql" not in text:
        suggestions.append(
            "Learn PostgreSQL for production applications."
        )

    if "kubernetes" not in text:
        suggestions.append(
            "Explore Kubernetes and deployment workflows."
        )

    score = max(0, score)

    for weakness in weaknesses:
        score -= 5

    if score < 0:
        score = 0

    max_score = 150

    score_percentage = round(
    (score / max_score) * 100
)

    score = score_percentage
    if career_paths:
        roadmap = generate_roadmap(career_paths[0])
    else:
        roadmap = [] 
    return {

    # ===========================
    # Main Scores
    # ===========================

    "score": score,

    "resume_quality":

    "Excellent" if score >= 90 else

    "Good" if score >= 75 else

    "Average" if score >= 60 else

    "Needs Improvement",

    "career_readiness":

    min(score + 5, 100),

    "skill_coverage":

    max(0, 100 - len(weaknesses) * 5),

    # ===========================
    # Analysis
    # ===========================

    "strengths": strengths,

    "weaknesses": weaknesses,

    "suggestions": suggestions,

    # ===========================
    # Career
    # ===========================

    "career_paths": career_paths,

    "projects": projects,

    "certifications": certifications,
    "roadmap": roadmap,

}