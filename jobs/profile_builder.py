from resumes.resume_analyzer import (
    extract_projects,
    extract_experience
)

def build_profile(resume):

    skills = [
        skill.name
        for skill in resume.skills.all()
    ]

    projects = extract_projects(
        resume.resume_text
    )

    experience = extract_experience(
        resume.resume_text
    )

    profile = f"""
    Skills:
    {', '.join(skills)}

    Projects:
    {' '.join(projects)}

    Experience:
    {' '.join(experience)}

    Career Goal:
    AI Developer
    Backend Developer
    Full Stack Developer
    """

    return profile