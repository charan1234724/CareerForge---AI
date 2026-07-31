from ai_agents.llm_service import ask_llm


def career_copilot(
    resume_text,
    job_description
):

    from ai_agents.llm_service import ask_llm


def career_copilot(
    resume_text,
    job_description
):

    prompt = f"""
You are a Senior AI Career Mentor, Technical Recruiter, and Software Engineering Hiring Manager.

Analyze the candidate's resume and compare it with the given job description.

==================================================

Candidate Resume

{resume_text}

==================================================

Job Description

{job_description}

==================================================

Generate the report in the EXACT format below.

🚀 CAREER MATCH

Overall Match Score:
/100

Recommended Career Role:

Career Readiness:
%

Expected Salary Range:

Hiring Probability:
%

--------------------------------------------------

💪 STRENGTHS

Provide 5 strengths.

--------------------------------------------------

⚠ MISSING SKILLS

Provide 5 important missing skills.

--------------------------------------------------

📚 LEARNING ROADMAP

Month 1

Month 2

Month 3

Month 4

--------------------------------------------------

💻 RECOMMENDED PROJECTS

Provide 5 projects.

--------------------------------------------------

🏆 RECOMMENDED CERTIFICATIONS

Provide 5 certifications.

--------------------------------------------------

🏢 TOP COMPANIES

Provide 10 companies.

--------------------------------------------------

🎤 INTERVIEW PREPARATION

Provide:

Technical Topics

HR Topics

Coding Topics

--------------------------------------------------

💡 AI RECOMMENDATIONS

Provide 8 recommendations.

Keep the report professional.

Do NOT use Markdown tables.

Use headings exactly as above.
"""

    return ask_llm(prompt)

    return ask_llm(
        prompt
    )