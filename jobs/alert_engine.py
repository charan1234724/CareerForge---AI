from django.core.mail import send_mail
from django.conf import settings


def send_job_alert(user, jobs):
    """
    Send an email containing newly matched jobs.
    """

    if not jobs:
        return

    lines = []

    for job in jobs:

        lines.append(
            f"""
Title : {job['title']}
Company : {job['company']}
Location : {job['location']}
Apply : {job['url']}
"""
        )

    message = "\n".join(lines)

    send_mail(
        subject="CareerForge AI - New Matching Jobs",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )