def calculate_match(resume_skills, job_skills):

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    job_set = {
        skill.strip().lower()
        for skill in job_skills
    }

    matched = resume_set.intersection(job_set)

    return round(
        len(matched) / len(job_set) * 100,
        2
    )