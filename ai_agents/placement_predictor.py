from ai_agents.llm_service import ask_llm


def predict_placement(resume_text):

    prompt = f"""

You are an expert placement mentor.

Analyze this resume.

Resume:

{resume_text}

Provide:

1. Placement Probability (0-100%)

2. Resume Strengths

3. Resume Weaknesses

4. Missing Skills

5. Improvement Suggestions

6. Recommended Certifications

7. Final Placement Readiness Score

Keep response concise.

"""

    return ask_llm(prompt)