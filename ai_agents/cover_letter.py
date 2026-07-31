from ai_agents.llm_service import ask_llm


def generate_cover_letter(
    resume_text,
    job_text
):

    prompt = f"""

You are a professional HR recruiter.

Generate a professional cover letter
for the candidate.

Candidate Resume:

{resume_text}

Target Job Description:

{job_text}

Requirements:

1. Professional tone

2. Mention relevant skills

3. Mention projects if relevant

4. Mention internship experience
if available

5. Explain why the candidate
fits the role

6. Keep under 350 words

7. Ready to submit

Generate only the cover letter.

"""

    return ask_llm(
        prompt
    )