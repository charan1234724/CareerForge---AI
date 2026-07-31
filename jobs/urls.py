from django.urls import path

from .views import (
    matched_jobs,
    real_jobs,
    skill_gap,
    job_details,
    resume_tailor_view,
    cover_letter_view,
    download_cover_letter_pdf,
    company_preparation,
    apply_job,
    download_company_preparation_pdf,
)

urlpatterns = [

    path(
        "matches/",
        matched_jobs,
        name="matches"
    ),

    path(
        "real-jobs/",
        real_jobs,
        name="real_jobs"
    ),

    path(
        "skill-gap/",
        skill_gap,
        name="skill_gap"
    ),

    path(
        "job-details/",
        job_details,
        name="job_details"
    ),
    path(
    "company-preparation/pdf/",
    download_company_preparation_pdf,
    name="download_company_preparation_pdf"
),

    path(
        "resume-tailor/",
        resume_tailor_view,
        name="resume_tailor"
    ),
    path(
    "cover-letter/",
    cover_letter_view,
    name="cover_letter"
),
    path(
    "download-cover-letter-pdf/",
    download_cover_letter_pdf,
    name="download_cover_letter_pdf"
),
    path(
    "company-preparation/",
    company_preparation,
    name="company_preparation"
),

    path(
        "apply-job/",
        apply_job,
        name="apply_job"
    )
]