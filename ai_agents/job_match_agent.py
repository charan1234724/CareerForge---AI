from google import genai
from decouple import config

client = genai.Client(
    api_key=config("GEMINI_API_KEY")
)
def analyze_job_match(
    resume_text,
    job_description
):

    prompt = f"""
    Compare this resume and job.

    Resume:
    {resume_text}

    Job:
    {job_description}

    Give:

    1. Match Score (0-100)
    2. Matched Skills
    3. Missing Skills
    4. Why this job fits
    5. Learning Suggestions

    Return concise output.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text