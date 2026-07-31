from data.interview_questions import (
    QUESTION_BANK,
    HR_QUESTIONS,
    PROJECT_QUESTIONS,
    INTERNSHIP_QUESTIONS
)

from ai_agents.llm_service import ask_llm


def generate_questions(resume):

    questions = []

    skills = [
        skill.name.lower()
        for skill in resume.skills.all()
    ]

    for skill in skills:

        if skill in QUESTION_BANK:

            skill_data = QUESTION_BANK[skill]

            if "technical" in skill_data:

                questions.extend(
                    skill_data["technical"]
                )

    text = resume.resume_text.lower()

    if "project" in text:

        questions.extend(
            PROJECT_QUESTIONS
        )

    if "intern" in text:

        questions.extend(
            INTERNSHIP_QUESTIONS
        )

    questions.extend(
        HR_QUESTIONS
    )

    return questions


def generate_ai_questions(
    resume_text,
    job_description=""
):

    prompt = f"""
You are a Senior Technical Interviewer at Google, Microsoft and Amazon.

Candidate Resume:

{resume_text[:2500]}

Job Description:

{job_description[:2500]}

Generate a professional interview.

Return in this order:

========================

Technical Questions
(5 Questions)

========================

Project Based Questions
(3 Questions)

========================

Internship Questions
(2 Questions)

========================

HR Questions
(3 Questions)

========================

Coding Questions
(2 Questions)

Rules:

- Questions must be based on candidate skills.
- Ask follow-up questions whenever possible.
- Keep questions interviewer style.
- Do not provide answers.
- Return clean formatted text.

"""

    return ask_llm(prompt)


def evaluate_answer(
    question,
    answer
):

    prompt = f"""
You are a Senior Software Engineering Interviewer.

Interview Question:

{question}

Candidate Answer:

{answer}

Evaluate using the following format:

Overall Score (0-10)

Technical Knowledge

Communication Skills

Confidence

Problem Solving

Strengths

Weaknesses

Correct Answer

Suggestions for Improvement

Final Interviewer Feedback

Keep it concise and professional.
"""

    return ask_llm(prompt)