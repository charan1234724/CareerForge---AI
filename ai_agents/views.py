from django.shortcuts import render

from resumes.models import Resume

from .career_copilot import (
    career_copilot
)
from .resume_tailor import (
    tailor_resume
)
from .interview_agent import (
    generate_questions,
    generate_ai_questions
)
from .cover_letter import (
    generate_cover_letter
)
from .interview_agent import (
    generate_questions,
    generate_ai_questions,
    evaluate_answer
)
from .placement_predictor import (
    predict_placement
)
from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from jobs.models import Job, CoverLetter
from reportlab.lib.styles import (
    getSampleStyleSheet
)
from .roadmap_agent import (
    generate_career_roadmap
)
from .portfolio_generator import generate_portfolio
from .recruiter_simulator import recruiter_simulator
from notifications.models import Notification
from ai_agents.career_roadmap import generate_roadmap
from ai_agents.placement_scoring import calculate_placement_scores

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from resumes.models import Resume
from ai_agents.resume_improver import analyze_resume_improvement
from accounts.models import StudentProfile

@login_required
def analytics(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/analytics.html",
            {
                "analysis": None
            }
        )

    analysis = analyze_resume_improvement(
        resume.resume_text
    )

    return render(
        request,
        "ai_agents/analytics.html",
        {
            "analysis": analysis
        }
    )
@login_required
def career_analysis(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/career_analysis.html",
            {
                "analysis": "",
                "career_score": 0,
                "salary": "N/A",
                "career": "Not Available",
                "readiness": 0,
            }
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    analysis = career_copilot(
        resume.resume_text[:2500],
        job_text[:2500]
    )

    # Temporary values
    career_score = 91
    readiness = 88
    salary = "₹8–12 LPA"
    career = "AI / ML Engineer"

    return render(
        request,
        "ai_agents/career_analysis.html",
        {
            "analysis": analysis,
            "career_score": career_score,
            "salary": salary,
            "career": career,
            "readiness": readiness,
        }
    )

from django.contrib.auth.decorators import login_required
from resumes.models import Resume

@login_required
def interview_prep(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/interview.html",
            {
                "questions": [],
                "ai_questions": "",
                "total_questions": 0,
                "technical_count": 0,
                "project_count": 0,
                "hr_count": 0,
            }
        )

    questions = generate_questions(resume)

    job_text = request.GET.get(
        "job_text",
        ""
    )

    ai_questions = generate_ai_questions(
        resume.resume_text,
        job_text
    )

    technical_count = sum(
        1 for q in questions
        if "technical" in q.get("category","").lower()
    )

    project_count = sum(
        1 for q in questions
        if "project" in q.get("category","").lower()
    )

    hr_count = sum(
        1 for q in questions
        if "hr" in q.get("category","").lower()
    )

    return render(
        request,
        "ai_agents/interview.html",
        {
            "questions": questions,
            "ai_questions": ai_questions,
            "total_questions": len(questions),
            "technical_count": technical_count,
            "project_count": project_count,
            "hr_count": hr_count,
        }
    )
from .resume_improver import (
    analyze_resume_improvement
)

def resume_improvement(request):

    resume = Resume.objects.last()

    if not resume:

        return render(
            request,
            "ai_agents/resume_improvement.html",
            {
                "result": None
            }
        )

    result = analyze_resume_improvement(
        resume.resume_text
    )

    return render(
        request,
        "ai_agents/resume_improvement.html",
        {
            "result": result
        }
    )
from django.contrib.auth.decorators import (
    login_required
)

from resumes.models import Resume


@login_required
def resume_tailoring(
    request
):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/resume_tailoring.html",
            {
                "result":
                "No Resume Uploaded"
            }
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    result = tailor_resume(
        resume.resume_text[:2500],
        job_text[:2500]
    )

    return render(
        request,
        "ai_agents/resume_tailoring.html",
        {
            "result": result
        }
    )
@login_required
def cover_letter(request):

    import hashlib

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:
        return render(
            request,
            "ai_agents/cover_letter.html",
            {
                "letter": "No Resume Uploaded"
            }
        )

    job_id = request.GET.get("job_id")

    if not job_id:
        return render(
            request,
            "ai_agents/cover_letter.html",
            {
                "letter": "Job not found."
            }
        )

    try:
        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:
        return render(
            request,
            "ai_agents/cover_letter.html",
            {
                "letter": "Invalid Job."
            }
        )

    # -----------------------------
    # Generate hashes
    # -----------------------------

    resume_hash = hashlib.sha256(
        resume.resume_text.encode()
    ).hexdigest()

    job_hash = hashlib.sha256(
        job.description.encode()
    ).hexdigest()

    # -----------------------------
    # Check cache
    # -----------------------------

    existing = CoverLetter.objects.filter(
        user=request.user,
        job=job,
        resume_hash=resume_hash,
        job_hash=job_hash,
    ).first()

    if existing:

        print("✅ Loaded Cover Letter from Database")

        return render(
            request,
            "ai_agents/cover_letter.html",
            {
                "letter": existing.content,
                "cached": True,
            }
        )

    # -----------------------------
    # Generate New Cover Letter
    # -----------------------------

    print("🤖 Generating Cover Letter using LLM...")

    letter = generate_cover_letter(
        resume.resume_text[:2500],
        job.description[:2500]
    )

    # -----------------------------
    # Save / Update Database
    # -----------------------------

    import traceback

    try:

        obj, created = CoverLetter.objects.update_or_create(
        user=request.user,
        job=job,
        defaults={
            "content": letter,
            "resume_hash": resume_hash,
            "job_hash": job_hash,
            "llm_model": "deepseek/deepseek-chat",
        }
    )

        print("✅ Saved:", obj.id, "Created:", created)

    except Exception as e:

        print("❌ DATABASE ERROR")
        print(e)
        traceback.print_exc()

    if created:
        print("✅ Cover Letter Saved")
    else:
        print("✅ Cover Letter Updated")

    return render(
        request,
        "ai_agents/cover_letter.html",
        {
            "letter": letter,
            "cached": False,
        }
    )
@login_required
def interview_feedback(request):

    result = None

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        )

        answer = request.POST.get(
            "answer",
            ""
        )

        result = evaluate_answer(
            question,
            answer
        )

    return render(
        request,
        "ai_agents/interview_feedback.html",
        {
            "result": result
        }
    )
@login_required
def placement_prediction(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/placement_prediction.html",
            {
                "result":
                "No Resume Uploaded"
            }
        )

    scores = calculate_placement_scores(
    resume.resume_text
)

    result = predict_placement(
    resume.resume_text[:2500]
)


    placement_score = scores["placement_score"]

    if placement_score >= 85:
        status = "Excellent"
    elif placement_score >= 70:
        status = "Good"
    elif placement_score >= 50:
        status = "Average"
    else:
        status = "Needs Improvement"

    return render(
    request,
    "ai_agents/placement_prediction.html",
    {
        "result": result,

        "placement_score": scores["placement_score"],

        "hiring_probability": scores["hiring_probability"],

        "interview_score": scores["interview_score"],

        "company_readiness": scores["company_readiness"],

        "salary": scores["salary"],

        "career": scores["career"],

        "strengths": scores["strengths"],

        "weaknesses": scores["weaknesses"],

        "projects": scores["projects"],

        "certifications": scores["certifications"],

        "status": status,
    }
)
@login_required
def download_placement_pdf(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return redirect(
            "placement_prediction"
        )

    result = predict_placement(
        resume.resume_text[:2500]
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="Placement_Report.pdf"'
    )

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "CareerForge AI Placement Prediction Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            result.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    doc.build(
        story
    )

    return response
@login_required
def career_roadmap(request, career=None):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/roadmap.html",
            {
                "career": None,
                "roadmap": [],
                "error": "No resume uploaded."
            }
        )

    # If opened from sidebar, use the first recommended career
    if career is None:

        result = analyze_resume_improvement(
            resume.resume_text
        )

        career_paths = result.get(
            "career_paths",
            []
        )

        if career_paths:
            career = career_paths[0]
        else:
            career = "AI Engineer"

    roadmap = generate_roadmap(career)

    Notification.objects.create(
        user=request.user,
        title="Career Roadmap",
        message=f"{career} roadmap generated successfully."
    )

    return render(
        request,
        "ai_agents/roadmap.html",
        {
            "career": career,
            "roadmap": roadmap
        }
    )
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from resumes.models import Resume
from .portfolio_generator import generate_portfolio
from .models import Portfolio

@login_required
def portfolio_generator(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/portfolio.html",
            {
                "portfolio": "No Resume Uploaded"
            }
        )

    saved_portfolio = Portfolio.objects.filter(
    user=request.user
).first()

    if saved_portfolio:

        portfolio = saved_portfolio.html

    else:

        portfolio = generate_portfolio(
        resume.resume_text[:2500]
    )

        Portfolio.objects.create(
        user=request.user,
        html=portfolio
    )

        Notification.objects.create(
        user=request.user,
        title="Portfolio Generated",
        message="Your AI portfolio is ready."
    )
    from accounts.models import StudentProfile

    profile = StudentProfile.objects.get(
    user=request.user
)

    analysis = []

# Resume

    if resume:
        analysis.append("✅ Resume uploaded successfully.")
    else:
        analysis.append("⚠ Upload a resume.")

# Skills

    if resume and resume.skills.count() >= 10:
        analysis.append("✅ Strong technical skill set detected.")
    elif resume:
        analysis.append("⚠ Add more technical skills to your resume.")

# GitHub
 
    if profile.github:
        analysis.append("✅ GitHub profile linked.")
    else:
        analysis.append("⚠ Add your GitHub profile.")

# LinkedIn

    if profile.linkedin:
        analysis.append("✅ LinkedIn profile linked.")
    else:
        analysis.append("⚠ Add your LinkedIn profile.")

# Portfolio Website

    if profile.portfolio:
        analysis.append("✅ Portfolio website configured.")
    else:
        analysis.append("⚠ Portfolio website not added.")

# Dream Role

    if profile.dream_role:
        analysis.append(
        f"🎯 Career goal: {profile.dream_role}"
    )
    
    
    portfolio_exists = Portfolio.objects.filter(
    user=request.user
).exists()

    return render(
    request,
    "ai_agents/portfolio.html",
    {
        "portfolio": portfolio,
        "portfolio_exists": portfolio_exists,
        "analysis": analysis,
    }
)
@login_required
def download_portfolio(request):

    portfolio = Portfolio.objects.filter(
    user=request.user
).first()

    if portfolio:

        html = portfolio.html

    else:

        html = "<h1>No Portfolio Generated</h1>"

    response = HttpResponse(
        html,
        content_type="text/html"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="CareerForge_Portfolio.html"'
    )

    return response
@login_required
def preview_portfolio(request):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    if profile.portfolio_visibility == "private":

        portfolio = Portfolio.objects.filter(
            user=request.user
        ).first()

    else:

        portfolio = Portfolio.objects.filter(
            user=request.user
        ).first()

    if portfolio:

        return HttpResponse(portfolio.html)

    return HttpResponse(
        "<h1>No Portfolio Generated</h1>"
    )
from django.contrib.auth.models import User


def public_portfolio(request, username):

    owner = User.objects.get(
        username=username
    )

    profile = StudentProfile.objects.get(
        user=owner
    )

    if profile.portfolio_visibility == "private":

        return HttpResponse(
            "<h2>This portfolio is private.</h2>",
            status=403
        )

    portfolio = Portfolio.objects.filter(
        user=owner
    ).first()

    if not portfolio:

        return HttpResponse(
            "<h2>No portfolio available.</h2>"
        )

    return HttpResponse(
        portfolio.html
    )

@login_required
def regenerate_portfolio(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return redirect("portfolio_generator")

    portfolio = generate_portfolio(
        resume.resume_text[:2500]
    )

    Portfolio.objects.update_or_create(

        user=request.user,

        defaults={

            "html": portfolio

        }

    )

    Notification.objects.create(

        user=request.user,

        title="Portfolio Regenerated",

        message="Your AI portfolio has been regenerated."

    )
    return redirect("portfolio_generator")
@login_required
def recruiter_ai(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "ai_agents/recruiter.html",
            {
                "result":
                "No Resume Uploaded"
            }
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    result = recruiter_simulator(
        resume.resume_text[:2500],
        job_text[:2500]
    )
    Notification.objects.create(

    user=request.user,

    title="Recruiter AI Completed",

    message="Your resume was evaluated by the AI Recruiter Simulator."

)

    return render(
        request,
        "ai_agents/recruiter.html",
        {
            "result": result
        }
    )