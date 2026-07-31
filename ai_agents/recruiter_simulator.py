from ai_agents.llm_service import ask_llm


def recruiter_simulator(
    resume_text,
    job_description
):

    prompt = f"""
You are an experienced technical recruiter.

Evaluate the candidate exactly as a recruiter would.

Resume:

{resume_text}

Job Description:

{job_description}

Return:

1. ATS Score (0-100)

2. Recruiter Score (0-100)

3. Resume Ranking
(Top 5%, Top 10%, Top 25%, etc.)

4. Shortlisting Chance

5. Strengths

6. Weaknesses

7. Missing Skills

8. Recruiter Feedback

9. Final Hiring Decision
(Strong Yes / Yes / Maybe / No)

Keep the response professional.
"""

    return ask_llm(prompt)