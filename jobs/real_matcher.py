def calculate_real_match(resume_skills, job_text):

    job_text = job_text.lower()

    matched_skills = []

    for skill in resume_skills:

        if skill.lower() in job_text:
            matched_skills.append(skill)

    if len(resume_skills) == 0:
        return 0, []

    score = round(
        (len(matched_skills) / len(resume_skills)) * 100,
        2
    )

    return score, matched_skills