from ai_agents.llm_service import ask_llm


def explain_job_fit(
    resume_text,
    job_title,
    job_description
):

    prompt = f"""
    Resume:

    {resume_text}

    Job Title:

    {job_title}

    Job Description:

    {job_description}

    Explain in 5 bullet points:

    1. Why this job matches the candidate
    2. Relevant skills from the resume
    3. Strengths of the candidate
    4. Missing skills (if any)
    5. Preparation tips before applying

    Keep the answer concise and professional.
    """

    return ask_llm(
        prompt
    )