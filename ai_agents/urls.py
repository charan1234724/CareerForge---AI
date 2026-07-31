from django.urls import path
from .views import analytics

from .views import (
    career_analysis,
    interview_prep,
    interview_feedback,
    resume_improvement,
    resume_tailoring,
    cover_letter,
    placement_prediction,
    download_placement_pdf,
    career_roadmap,
    portfolio_generator,
    download_portfolio,
    preview_portfolio,
    recruiter_ai,
    regenerate_portfolio,
    public_portfolio,
)

urlpatterns = [

    path(
        "career-analysis/",
        career_analysis,
        name="career_analysis"
    ),
    path(
    "analytics/",
    analytics,
    name="analytics"
),
    path(
    "regenerate-portfolio/",
    regenerate_portfolio,
    name="regenerate_portfolio",
),
    path(
        "interview-prep/",
        interview_prep,
        name="interview_prep"
    ),
    path(
    "portfolio/<str:username>/",
    public_portfolio,
    name="public_portfolio",
),

    path(
        "interview-feedback/",
        interview_feedback,
        name="interview_feedback"
    ),

    path(
        "resume-tailoring/",
        resume_tailoring,
        name="resume_tailoring"
    ),

    path(
        "resume-improvement/",
        resume_improvement,
        name="resume_improvement"
    ),

    path(
        "cover-letter/",
        cover_letter,
        name="cover_letter"
    ),

    path(
        "placement-prediction/",
        placement_prediction,
        name="placement_prediction"
    ),
    path(
    "download-placement-pdf/",
    download_placement_pdf,
    name="download_placement_pdf"
),
    path(
    "career-roadmap/",
    career_roadmap,
    name="career_roadmap",
),

    path(
    "career-roadmap/<str:career>/",
    career_roadmap,
    name="career_roadmap_detail",
),
    path(
    "portfolio-generator/",
    portfolio_generator,
    name="portfolio_generator"
),

    path(
    "download-portfolio/",
    download_portfolio,
    name="download_portfolio"
),

    path(
    "preview-portfolio/",
    preview_portfolio,
    name="preview_portfolio"
),
    path(
    "recruiter-ai/",
    recruiter_ai,
    name="recruiter_ai"
),
]