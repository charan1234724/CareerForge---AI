from django.contrib.auth import login
from ai_agents.score_engine import calculate_resume_scores
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.contrib import messages
import json
from datetime import datetime
import pytz
from .forms import BugReportForm
from .forms import SupportTicketForm
from .models import SupportTicket
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import traceback
from ai_agents.score_engine import calculate_resume_scores
from django.http import HttpResponse
from ai_agents.models import Portfolio
def signup(request):

    if request.method=="POST":

        form=SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "🎉 Account created successfully! Please login to continue."
            )

            return redirect("login")

    else:

        form=SignUpForm()

    return render(

        request,

        "accounts/signup.html",

        {

            "form":form

        }

    )
from resumes.models import Resume
from accounts.models import StudentProfile

@login_required
def dashboard(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        "resume_uploaded": resume is not None,
        "resume": resume,
        "profile": profile,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )
from .models import StudentProfile
from .forms import StudentProfileForm
from resumes.models import Resume
from applications.models import Application
import io
import json
import zipfile

from django.http import HttpResponse

@login_required
def profile(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            profile = form.save()

            print("SUCCESS")
            print(profile.profile_picture)

            return redirect("profile")

        else:

            print("FORM ERRORS")
            print(form.errors)

    else:

        form = StudentProfileForm(instance=profile)

    # ----------------------------
    # Resume Information
    # ----------------------------

    resume = Resume.objects.filter(user=request.user).last()

    resume_uploaded = resume is not None
    # ----------------------------
    # Profile Completion
    # ----------------------------

    completed = 0
    total = 30

# Personal Information (10 Points)

    if profile.profile_picture:
        completed += 2

    if profile.phone:
        completed += 1

    if profile.college:
        completed += 2

    if profile.branch:
        completed += 2

    if profile.graduation_year:
        completed += 1

    if profile.cgpa:
        completed += 2


    # Career Information (8 Points)

    if profile.location:
        completed += 1

    if profile.dream_company:
        completed += 2

    if profile.dream_role:
        completed += 2

    if profile.bio:
        completed += 3


    # Professional Links (6 Points)

    if profile.linkedin:
        completed += 2

    if profile.github:
        completed += 2

    if profile.portfolio:
        completed += 2


    # Resume (6 Points)

    if resume_uploaded:
        completed += 6


    profile_completion = round((completed / total) * 100)

    from ai_agents.score_engine import calculate_resume_scores

    if resume_uploaded:

        scores = calculate_resume_scores(resume)

        resume_score = scores.resume_score

        placement_score = scores.placement_score

        skills_count = resume.skills.count()

    else:

        resume_score = None

        placement_score = None

        skills_count = 0

    # ----------------------------
    # Applications
    # ----------------------------

    applications_count = Application.objects.filter(
    user=request.user
).count()

    return render(

        request,

        "accounts/profile.html",

        {

            "form": form,

            "profile": profile,

            "resume_uploaded": resume_uploaded,

            "resume_score": resume_score,

            "placement_score": placement_score,

            "skills_count": skills_count,

            "applications_count": applications_count,
            "profile_completion": profile_completion,

        }

    )
from django.contrib import messages
from resumes.models import Resume
from applications.models import Application, SavedJob
from ai_agents.score_engine import calculate_resume_scores


@login_required
def settings_view(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            print("FORM IS VALID")

            print(form.cleaned_data)

            form.save()

            messages.success(
        request,
        "Settings updated successfully."
    )

            return redirect("settings")

        else:

            print("FORM ERRORS:")

            print(form.errors)

    else:

        form = StudentProfileForm(
            instance=profile
        )

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    resume_uploaded = resume is not None

    applications_count = Application.objects.filter(
        user=request.user
    ).count()

    saved_jobs_count = SavedJob.objects.filter(
        user=request.user
    ).count()

    if resume_uploaded:

        scores = calculate_resume_scores(
            resume
        )

        resume_score = scores.resume_score

        placement_score = scores.placement_score

        skills_count = resume.skills.count()

    else:

        resume_score = None

        placement_score = None

        skills_count = 0

    return render(

        request,

        "accounts/settings.html",

        {

            "form": form,

            "profile": profile,

            "resume_uploaded": resume_uploaded,

            "resume": resume,

            "resume_score": resume_score,

            "placement_score": placement_score,

            "applications_count": applications_count,

            "saved_jobs_count": saved_jobs_count,

            "skills_count": skills_count,

        }

    )
from django.contrib.auth import logout


@login_required
def delete_account(request):

    if request.method == "POST":

        user = request.user

        logout(request)

        user.delete()

        return redirect("login")

    return render(
        request,
        "accounts/delete_account.html"
    )
from django.conf import settings
def custom_password_reset(request):
    raise Exception("CUSTOM PASSWORD RESET VIEW IS RUNNING")
    print("PASSWORD RESET VIEW CALLED")
    

    if request.method == "POST":

        email = request.POST.get("email")
        print("User found:", user.email)

        print("Creating email...")

        print("About to send email...")

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            messages.error(
                request,
                "❌ No account found with this email."
            )

            return redirect("password_reset")

        current_site = get_current_site(request)

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        reset_link = request.build_absolute_uri(
    f"/reset/{uid}/{token}/"
)

        subject = "CareerForge AI - Password Reset"

        text_content = render_to_string(

            "registration/password_reset_email.txt",

            {

                "user": user,

                "reset_link": reset_link,

            }

        )

        html_content = render_to_string(

            "registration/password_reset_email.html",

            {

                "user": user,

                "reset_link": reset_link,

            }

        )

        message = EmailMultiAlternatives(
    subject=subject,
    body=text_content,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[user.email],
)

        message.attach_alternative(
    html_content,
    "text/html"
)

        try:
            sent = message.send(fail_silently=False)
            print("EMAIL SEND RESULT:", sent)

            messages.success(
        request,
        "✅ Password reset link sent successfully."
    )

            return redirect("password_reset_done")

        except Exception as e:
            traceback.print_exc()

            messages.error(
        request,
        f"Email sending failed: {e}"
    )

            return redirect("password_reset")

    return render(

        request,

        "registration/password_reset_form.html"

    )
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


@login_required
def update_ai_preferences(request):

    if request.method != "POST":

        return JsonResponse({
            "status": "error"
        }, status=400)

    try:

        data = json.loads(request.body)

        field = data.get("field")

        value = data.get("value")

        profile = request.user.studentprofile

        allowed_fields = [

    # AI Preferences

    "ai_resume_analysis",

    "ai_career_recommendations",

    "ai_job_matching",

    "smart_notifications",

    # Notification Preferences

    "email_notifications",

    "job_alerts",

    "interview_reminders",

    "weekly_report",

]

        if field not in allowed_fields:

            return JsonResponse({

                "status": "invalid_field"

            }, status=400)

        setattr(profile, field, value)

        profile.save()

        return JsonResponse({

            "status": "success",

            "field": field,

            "value": value

        })

    except Exception as e:

        return JsonResponse({

            "status": "error",

            "message": str(e)

        }, status=500)

@login_required
def download_my_data(request):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    applications = Application.objects.filter(
        user=request.user
    )

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    )

    data = {

        "username": request.user.username,

        "email": request.user.email,

        "phone": profile.phone,

        "college": profile.college,

        "branch": profile.branch,

        "graduation_year": profile.graduation_year,

        "cgpa": str(profile.cgpa),

        "location": profile.location,

        "dream_company": profile.dream_company,

        "dream_role": profile.dream_role,

        "linkedin": profile.linkedin,

        "github": profile.github,

        "portfolio": profile.portfolio,

        "bio": profile.bio,

        "resume_uploaded": resume is not None,

        "skills": [

            skill.name

            for skill in resume.skills.all()

        ] if resume else [],

        "applications": [

            {

                "title": app.title,

                "company": app.company,

                "status": app.status

            }

            for app in applications

        ],

        "saved_jobs": [

            {

                "title": job.title,

                "company": job.company

            }

            for job in saved_jobs

        ]

    }

    response = HttpResponse(

        json.dumps(

            data,

            indent=4

        ),

        content_type="application/json"

    )

    response["Content-Disposition"] = (

        'attachment; filename="CareerForge_Data.json"'

    )

    return response
from datetime import datetime
@login_required
def export_profile(request):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    applications = Application.objects.filter(
        user=request.user
    ).count()

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).count()

    skills = 0
    skills_list = []
    resume_score = 0
    placement_score = 0

    if resume:

        scores = calculate_resume_scores(
            resume
        )

        resume_score = scores.resume_score

        placement_score = scores.placement_score

        skills = resume.skills.count()

        skills_list = [

        skill.name

        for skill in resume.skills.all()

]

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="CareerForge_Profile.pdf"'
    )

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
    Paragraph(
        "<font size=24 color='#2563EB'><b>CareerForge AI</b></font>",
        styles["Title"]
    )
)

    story.append(
    Paragraph(
        "<font size=16><b>Professional Career Report</b></font>",
        styles["Heading1"]
    )
)

    story.append(
    Paragraph(
        "Generated using CareerForge AI Career Intelligence Platform",
        styles["Italic"]
    )
)

    story.append(
    Spacer(1, 20)
)
    story.append(
    Paragraph(
        f"<b>Generated On:</b> {datetime.now().strftime('%d %B %Y %I:%M %p')}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"<b>Candidate:</b> {request.user.get_full_name() or request.user.username}",
        styles["BodyText"]
    )
)

    story.append(
    Spacer(1, 15)
)

    story.append(
        Spacer(1,20)
    )
    # ==========================
    # Profile Picture
    # ==========================

    if profile.profile_picture:

        try:

            img = Image(
            profile.profile_picture.path,
            width=110,
            height=110
        )

            story.append(img)

            story.append(
            Spacer(1,15)
        )

        except:

            pass
    story.append(
    Paragraph(
        "<font color='#2563EB'><b>PERSONAL INFORMATION</b></font>",
        styles["Heading2"]
    )
)

    story.append(
    Spacer(1,10)
)

    story.append(
        Paragraph(
            f"<b>Name:</b> {request.user.get_full_name() or request.user.username}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {request.user.email}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Phone:</b> {profile.phone}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>College:</b> {profile.college}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Branch:</b> {profile.branch}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Graduation:</b> {profile.graduation_year}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>CGPA:</b> {profile.cgpa}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Dream Company:</b> {profile.dream_company}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Dream Role:</b> {profile.dream_role}",
            styles["BodyText"]
        )
    )
    story.append(
    Spacer(1,15)
)

    story.append(
    Paragraph(
        "<font color='#2563EB'><b>EDUCATION</b></font>",
        styles["Heading2"]
    )
)

    story.append(
    Paragraph(
        f"College : {profile.college}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"Branch : {profile.branch}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"Graduation Year : {profile.graduation_year}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"CGPA : {profile.cgpa}",
        styles["BodyText"]
    )
)

    story.append(
        Spacer(1,20)
    )

    story.append(
    Paragraph(
        "<font color='#2563EB'><b>CAREER STATISTICS</b></font>",
        styles["Heading2"]
    )
)

    stats = [

    ["Resume Score", f"{resume_score}%"],

    ["Placement Score", f"{placement_score}%"],

    ["Skills", str(skills)],

    ["Applications", str(applications)],

    ["Saved Jobs", str(saved_jobs)],

]

    stats_table = Table(

    stats,

    colWidths=[220,120]

)

    stats_table.setStyle(

        TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("TEXTCOLOR",(0,0),(-1,-1),colors.darkblue),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("TOPPADDING",(0,0),(-1,-1),10),

        ("ALIGN",(1,0),(1,-1),"CENTER"),

    ])

)

    story.append(stats_table)
    story.append(
    Spacer(1,20)
)

    story.append(
    Paragraph(
        "<font color='#2563EB'><b>CAREER STATUS</b></font>",
        styles["Heading2"]
    )
)

    if placement_score >= 90:

        status = "★★★★★ Excellent Candidate"

    elif placement_score >= 75:

        status = "★★★★ Placement Ready"

    elif placement_score >= 60:

        status = "★★★ Developing Profile"

    else:

        status = "★★ Build More Skills"

    story.append(
    Paragraph(
        status,
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        "<font color='#2563EB'><b>TECHNICAL SKILLS</b></font>",
        styles["Heading2"]
    )
)
    if skills_list:

        skills_text = " • ".join(

        skills_list

    )

    else:
 
        skills_text = "No skills extracted from resume."

    story.append(

        Paragraph(

        skills_text,

        styles["BodyText"]

    )

)

    story.append(
        Spacer(1,20)
    )


    story.append(
    Paragraph(
        "<font color='#2563EB'><b>PROFESSIONAL LINKS</b></font>",
        styles["Heading2"]
    )
)

    story.append(
    Paragraph(
        f"LinkedIn : {profile.linkedin or 'Not Added'}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"GitHub : {profile.github or 'Not Added'}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        f"Portfolio : {profile.portfolio or 'Not Added'}",
        styles["BodyText"]
    )
)

    story.append(
    Paragraph(
        "<font color='#2563EB'><b>AI CAREER SUMMARY</b></font>",
        styles["Heading2"]
    )
)

    if placement_score >= 90:

        summary = (
        "Excellent placement readiness. "
        "Recommended for Product-Based Companies "
        "and AI/ML Software Engineering roles."
    )

    elif placement_score >= 75:

        summary = (
        "Good placement readiness. "
        "Strengthen projects and interview skills "
        "to become highly competitive."
    )

    elif placement_score >= 60:

        summary = (
        "Moderate profile. "
        "Improve technical skills and resume quality "
        "to increase hiring chances."
    )

    else:

        summary = (
        "Career profile is still developing. "
        "Focus on building projects, learning in-demand "
        "skills, and improving your resume."
    )

    story.append(
    Paragraph(
        summary,
        styles["BodyText"]
    )
)
    story.append(
    Spacer(1,30)
)

    story.append(
    Paragraph(
        "<font color='grey'>Generated by CareerForge AI</font>",
        styles["Italic"]
    )
)

    story.append(
    Paragraph(
        "<font color='grey'>Version 3.0 | AI Career Intelligence Platform</font>",
        styles["Italic"]
    )
)
    story.append(
    Spacer(1,10)
)

    story.append(
    Paragraph(
        "<font size=8 color='grey'>Confidential - Generated for Career Development Purposes Only</font>",
        styles["Italic"]
    )
)

    doc.build(
        story
    )

    return response

@login_required
def backup_data(request):

    profile = StudentProfile.objects.get(
        user=request.user
    )

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    portfolio = Portfolio.objects.filter(
        user=request.user
    ).first()

    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        profile_data = {

            "username": request.user.username,

            "email": request.user.email,

            "phone": profile.phone,

            "college": profile.college,

            "branch": profile.branch,

            "graduation_year": profile.graduation_year,

            "cgpa": str(profile.cgpa),

            "location": profile.location,

            "dream_company": profile.dream_company,

            "dream_role": profile.dream_role,

            "bio": profile.bio,

            "linkedin": profile.linkedin,

            "github": profile.github,

            "portfolio": profile.portfolio,

        }

        zip_file.writestr(

            "profile.json",

            json.dumps(
                profile_data,
                indent=4
            )

        )

        if portfolio:

            zip_file.writestr(

                "portfolio.html",

                portfolio.html

            )

        if resume:

            zip_file.writestr(

                "resume.txt",

                resume.resume_text

            )

    buffer.seek(0)

    response = HttpResponse(

        buffer.getvalue(),

        content_type="application/zip"

    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="CareerForge_Backup.zip"'

    return response

@login_required
def help_center(request):

    return render(
        request,
        "accounts/help_center.html"
    )
@login_required
def contact_support(request):

    if request.method == "POST":

        form = SupportTicketForm(request.POST)

        if form.is_valid():

            ticket = form.save(commit=False)

            ticket.user = request.user

            ticket.save()

            messages.success(

                request,

                "Support request submitted successfully."

            )

            return redirect("contact_support")

    else:

        form = SupportTicketForm()

    return render(

        request,

        "accounts/contact_support.html",

        {

            "form": form

        }

    )

@login_required
def faq(request):

    return render(
        request,
        "accounts/faq.html"
    )

@login_required
def report_bug(request):

    if request.method == "POST":

        form = BugReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            bug = form.save(commit=False)

            bug.user = request.user

            bug.save()

            messages.success(

                request,

                "Bug report submitted successfully."

            )

            return redirect("report_bug")

    else:

        form = BugReportForm()

    return render(

        request,

        "accounts/report_bug.html",

        {

            "form": form

        }

    )
