from ai_agents.llm_service import ask_llm


def tailor_resume(
    resume_text,
    job_text
):

    prompt = f"""

You are an expert ATS Resume Reviewer.

Compare the candidate resume and
the target job description.

Resume:

{resume_text}

Job Description:

{job_text}

Provide:

1. Overall Match Score (0-100)

2. Matching Skills

3. Missing Skills

4. Missing Keywords

5. ATS Optimization Suggestions

6. Resume Improvement Suggestions

7. Recommended Certifications

8. Recommended Projects

9. Final Recommendation

Format clearly with headings.

Keep the response professional.
"""

    return ask_llm(
        prompt
    )