from resumes.models import Resume
from jobs.alert_engine import send_job_alert




MATCH_THRESHOLD = 80


def check_user_jobs(user, jobs):
    from jobs.embedding_matcher import calculate_embedding_match

    try:

        resume = Resume.objects.get(user=user)

    except Resume.DoesNotExist:

        return

    matched = []

    for job in jobs:

        score = calculate_embedding_match(
    resume.resume_text,
    job["description"],
)

        if score >= MATCH_THRESHOLD:

            matched.append(job)

    if matched:

        send_job_alert(user, matched)