from django.urls import path

from .views import (
    upload_resume,
    resume_summary,
    delete_resume,
    download_resume_pdf
)
urlpatterns = [

    path(
        "upload-resume/",
        upload_resume,
        name="upload_resume"
    ),

    path(
        "resume-summary/",
        resume_summary,
        name="resume_summary"
    ),
    path(
        "delete-resume/",
        delete_resume,
        name="delete_resume"
    ),
    path(
    "download-resume-pdf/",
    download_resume_pdf,
    name="download_resume_pdf"
),
]