from ai_agents.llm_service import ask_llm


def generate_career_roadmap(
    resume_text
):

    prompt = f"""
    Analyze this resume.

    Resume:

    {resume_text}

    Generate a professional roadmap.

    Include:

    1. Career Goal

    2. Current Level

    3. Placement Readiness

    4. 30-Day Plan

    5. 60-Day Plan

    6. 90-Day Plan

    7. Certifications

    8. Projects

    9. Companies to Target

    Keep the answer clear with bullet points.
    """

    return ask_llm(prompt)