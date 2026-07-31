from ai_agents.llm_service import ask_llm


def analyze_skill_gap(
    resume_text,
    job_description
):

    prompt = f"""
    Compare the candidate resume and job description.

    Resume:

    {resume_text}

    Job Description:

    {job_description}

    Provide:

    1. Match Score (%)

    2. Matched Skills

    3. Missing Skills

    4. Learning Roadmap

    5. Recommended Certifications

    6. Recommended Projects

    7. Final Recommendation

    Keep the response clear, concise, and professional.
    """

    return ask_llm(
        prompt
    )