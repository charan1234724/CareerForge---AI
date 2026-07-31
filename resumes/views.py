from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Resume
from .forms import ResumeForm
from accounts.privacy import can_view_resume
from ai_agents.ats_checker import calculate_ats_score
from django.http import HttpResponseForbidden
from .resume_analyzer import (
    extract_education,
    extract_projects,
    extract_experience
)
from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)
from activity.models import Activity
from notifications.models import Notification
from ai_agents.score_engine import calculate_resume_scores
from ai_agents.resume_parser import (
    extract_resume_data
)
@login_required
def upload_resume(request):

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(
                commit=False
            )

            resume.user = request.user

            resume.save()
            Activity.objects.create(

    user=request.user,

    action="Resume Uploaded",

    description="Uploaded a new resume."

)           
            Notification.objects.create(
    user=request.user,
    title="Resume Uploaded",
    message="Your resume was uploaded successfully."
)

            return redirect(
                "resume_summary"
            )

    else:

        form = ResumeForm()

    return render(
        request,
        "resumes/upload_resume.html",
        {
            "form": form
        }
    )


@login_required
def resume_summary(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()
    owner = request.user

    if not can_view_resume(owner, request.user):

        return HttpResponseForbidden(
        "You don't have permission to view this resume."
    )

    if not resume:

        return render(
            request,
            "resumes/summary.html",
            {
                "resume": None,
                "ai_analysis": "No resume uploaded."
            }
        )

    # ==============================
    # Unified Score Engine
    # ==============================

    scores = calculate_resume_scores(
        resume
    )
    # Parse Resume

    resume_data = extract_resume_data(
    resume
)
    ats_score = scores.ats_score

    resume_score = scores.resume_score

    placement_score = scores.placement_score

    career_score = scores.career_score

    health_score = scores.health_score

    profile_completion = scores.profile_completion

    skill_match = scores.skill_match

    # ==============================
    # ATS Feedback
    # ==============================

    ats_feedback = []

    if ats_score < 70:

        ats_feedback.append(
            "Add more technical skills."
        )

    if profile_completion < 80:

        ats_feedback.append(
            "Complete your GitHub and LinkedIn profile."
        )

    if skill_match < 70:

        ats_feedback.append(
            "Improve industry-demand skills."
        )

    if ats_score >= 90:

        ats_feedback.append(
            "Excellent ATS Optimization."
        )

    # ==============================
    # Resume Information
    # ==============================
    education = resume_data.education

    projects = resume_data.projects

    experience = resume_data.experience
    # ==============================
    # AI Analysis
    # ==============================

    ai_analysis = """
Resume uploaded successfully.

Skills extracted successfully.

Education, Projects and Experience detected.

Use Resume Improvement Agent for detailed recommendations.
"""

    # ==============================
    # Render Page
    # ==============================

    return render(
        request,
        "resumes/summary.html",
        {

            "resume": resume,

            "ai_analysis": ai_analysis,

            "education": education,

            "projects": projects,

            "experience": experience,

            "ats_score": ats_score,

            "resume_score": resume_score,

            "placement_score": placement_score,

            "career_score": career_score,

            "health_score": health_score,

            "profile_completion": profile_completion,

            "skill_match": skill_match,

            "ats_feedback": ats_feedback,

        }
    )

@login_required
def delete_resume(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if resume:
        resume.delete()

    return redirect(
        "dashboard"
    )
@login_required
def download_resume_pdf(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return redirect(
            "resume_summary"
        )

    ats_score, ats_feedback = calculate_ats_score(
        resume.resume_text
    )

    education = extract_education(
        resume.resume_text
    )

    projects = extract_projects(
        resume.resume_text
    )

    experience = extract_experience(
        resume.resume_text
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="CareerForge_Report.pdf"'
    )

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "CareerForge AI Resume Analysis Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            f"ATS Score: {ats_score}",
            styles["Heading2"]
        )
    )

    feedback_text = "<br/>".join(
    ats_feedback
)

    story.append(
    Paragraph(
        feedback_text,
        styles["BodyText"]
    )
)

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            "Education",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            str(education),
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            "Projects",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            str(projects),
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            "Experience",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            str(experience),
            styles["BodyText"]
        )
    )

    doc.build(
        story
    )

    return response