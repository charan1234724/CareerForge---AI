from django.utils import timezone
from .models import Job


def sync_jobs(job_list):
    """
    Synchronize latest jobs with the database.
    """

    now = timezone.now()

    current_job_ids = []

    for job in job_list:

        provider = job.get("source", "Adzuna")

        provider_job_id = (
            job.get("id")
            or job.get("url")
            or f"{provider}_{job.get('title')}_{job.get('company')}"
        )

        current_job_ids.append(provider_job_id)

        Job.objects.update_or_create(
            provider_job_id=provider_job_id,
            defaults={
                "provider": provider,
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "description": job.get("description"),
                "required_skills": "",
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "url": job.get("url"),
                "source": provider,
                "last_seen": now,
                "is_active": True,
            },
        )

    return current_job_ids

from datetime import timedelta


def deactivate_old_jobs(days=7):
    """
    Mark jobs inactive if they haven't appeared recently.
    """

    cutoff = timezone.now() - timedelta(days=days)

    Job.objects.filter(
        last_seen__lt=cutoff,
        is_active=True
    ).update(is_active=False)