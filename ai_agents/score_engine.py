from dataclasses import dataclass
from ai_agents.resume_parser import extract_resume_data


@dataclass
class ResumeScores:

    ats_score: int

    resume_score: int

    profile_completion: int

    placement_score: int

    career_score: int

    health_score: int

    skill_match: int


# -------------------------
# ATS SCORE
# -------------------------

def calculate_ats(data):

    score = 0

    if data.email:
        score += 10

    if data.phone:
        score += 10

    if data.github:
        score += 10

    if data.linkedin:
        score += 10

    if len(data.skills) >= 5:
        score += 20

    if len(data.projects) >= 2:
        score += 15

    if len(data.education) >= 1:
        score += 15

    if len(data.experience) >= 1:
        score += 10

    return min(score, 100)


# -------------------------
# PROFILE COMPLETION
# -------------------------

def calculate_profile(data):

    score = 0

    if data.name:
        score += 20

    if data.email:
        score += 20

    if data.phone:
        score += 20

    if data.github:
        score += 20

    if data.linkedin:
        score += 20

    return min(score, 100)


# -------------------------
# RESUME QUALITY
# -------------------------

def calculate_resume_score(
    ats,
    profile
):

    return round(

        ats * 0.7 +

        profile * 0.3

    )


# -------------------------
# SKILL MATCH
# -------------------------

def calculate_skill_match(data):

    industry = [

        "python",

        "django",

        "react",

        "sql",

        "git",

        "docker",

        "aws",

        "machine learning",

        "tensorflow",

        "rest api"

    ]

    found = 0

    skills = [

        s.lower()

        for s in data.skills

    ]

    for skill in industry:

        if skill in skills:

            found += 1

    return round(

        found /

        len(industry)

        * 100

    )


# -------------------------
# HEALTH SCORE
# -------------------------

def calculate_health(

    ats,

    resume,

    skill

):

    return round(

        (

            ats +

            resume +

            skill

        ) / 3

    )


# -------------------------
# PLACEMENT SCORE
# -------------------------

def calculate_placement(

    ats,

    resume,

    skill,

    health

):

    return round(

        (

            ats +

            resume +

            skill +

            health

        ) / 4

    )


# -------------------------
# CAREER SCORE
# -------------------------

def calculate_career(

    placement,

    profile

):

    return round(

        (

            placement +

            profile

        ) / 2

    )


# -------------------------
# MAIN FUNCTION
# -------------------------

def calculate_resume_scores(

    resume

):

    data = extract_resume_data(

        resume

    )

    ats = calculate_ats(

        data

    )

    profile = calculate_profile(

        data

    )

    resume_score = calculate_resume_score(

        ats,

        profile

    )

    skill = calculate_skill_match(

        data

    )

    health = calculate_health(

        ats,

        resume_score,

        skill

    )

    placement = calculate_placement(

        ats,

        resume_score,

        skill,

        health

    )

    career = calculate_career(

        placement,

        profile

    )

    return ResumeScores(

        ats_score=ats,

        resume_score=resume_score,

        profile_completion=profile,

        placement_score=placement,

        career_score=career,

        health_score=health,

        skill_match=skill

    )