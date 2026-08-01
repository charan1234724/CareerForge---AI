from django.shortcuts import render
from resumes.models import Resume
from jobs.models import Job

from .matcher import calculate_match
from .job_search import search_jobs
from .real_matcher import calculate_real_match
from ai_agents.skill_gap_agent import (
    analyze_skill_gap
)


from jobs.profile_builder import (
    build_profile
)
from ai_agents.resume_tailor import (
    tailor_resume
)
from ai_agents.cover_letter import (
    generate_cover_letter
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
from notifications.models import Notification

from jobs.models import CompanyPreparation
from ai_agents.llm_service import ask_llm   # Replace ask_llm with your actual function name
from django.shortcuts import redirect
from applications.models import Application
from .cache_engine import (
    query_cache_valid,
    get_cached_jobs,
    update_query_cache,
)
from .models import Job, CoverLetter
def matched_jobs(request):

    resume = Resume.objects.last()

    if not resume:
        return render(
            request,
            "jobs/matches.html",
            {"matches": []}
        )

    resume_skills = [
        skill.name
        for skill in resume.skills.all()
    ]

    matches = []

    for job in Job.objects.all():

        job_skills = job.required_skills.split(",")

        score = calculate_match(
            resume_skills,
            job_skills
        )

        matches.append({
            "job": job,
            "score": score
        })

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render(
        request,
        "jobs/matches.html",
        {
            "matches": matches,
            "resume_skills": resume_skills
        }
    )
from .indianapi import search_indianapi
from .sync_engine import sync_jobs, deactivate_old_jobs
def real_jobs(request):
    print("=== real_jobs() called ===")

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:
        return render(
            request,
            "jobs/real_jobs.html",
            {
                "jobs": []
            }
        )

    profile_text = build_profile(resume)

    search_query = request.GET.get(
        "query",
        "python developer india"
    )
    if query_cache_valid(search_query):

        cached_jobs = get_cached_jobs(search_query)
        print("Cached Jobs:", len(cached_jobs))

        jobs = []

        for job in cached_jobs:

            jobs.append({
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "url": job.url,
            "source": job.source,
        })

    else:

        jobs = search_jobs(search_query)
        print("API Jobs:", len(jobs))

        sync_jobs(jobs)
        update_query_cache(search_query)

        deactivate_old_jobs()

    

    matched_jobs = []
    print("Jobs Before Matching:", len(jobs))
    print(jobs[:2])   # show first 2 jobs

    for job in jobs:
        job_text = (
            job.get("title", "")
            + " "
            + job.get("description", "")
        ).lower()

        score = calculate_embedding_match(
            profile_text,
            job_text
        )
        

        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        if salary_min and salary_max:
            salary = f"₹{salary_min:,} - ₹{salary_max:,}"
        elif salary_min:
            salary = f"₹{salary_min:,}+"
        else:
            salary = "Salary Not Disclosed"

        db_job = Job.objects.filter(
    url=job.get("url")
).first()

        matched_jobs.append({
            "id": db_job.id if db_job else None,

            "title": job.get(
                "title",
                "Unknown"
            ),

            "company": job.get(
                "company",
                "Unknown"
            ),

            "location": job.get(
                "location",
                "India"
            ),

            "salary": salary,

            "type": job.get(
                "type",
                "Full Time"
            ),

            "url": job.get(
                "url",
                "#"
            ),

            "score": score,

            "job_text": job_text,

            "recommended": False

        })

    matched_jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if matched_jobs:
        matched_jobs[0]["recommended"] = True

    print("Matched Jobs:", len(matched_jobs))
    print("Search Query:", search_query)

    return render(
        request,
        "jobs/real_jobs.html",
        {
            "jobs": matched_jobs[:20],
            "query": search_query
        }
    )
from django.contrib.auth.decorators import login_required


@login_required
def skill_gap(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "jobs/skill_gap.html",
            {
                "analysis": "No resume uploaded."
            }
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    analysis = analyze_skill_gap(
        resume.resume_text,
        job_text
    )

    return render(
        request,
        "jobs/skill_gap.html",
        {
            "analysis": analysis
        }
    )
def job_details(request):

    title = request.GET.get(
        "title",
        "Unknown Job"
    )

    company = request.GET.get(
        "company",
        "Unknown Company"
    )

    score = request.GET.get(
        "score",
        "0"
    )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    return render(
        request,
        "jobs/job_details.html",
        {
            "title": title,
            "company": company,
            "score": score,
            "job_text": job_text
        }
    )
from django.contrib.auth.decorators import login_required


@login_required
def resume_tailor_view(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return render(
            request,
            "jobs/resume_tailor.html",
            {
                "analysis":
                "No resume uploaded."
            }
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    if not job_text:

        return render(
            request,
            "jobs/resume_tailor.html",
            {
                "analysis":
                "Select a job first."
            }
        )

    analysis = tailor_resume(
        resume.resume_text,
        job_text
    )
    Notification.objects.create(

    user=request.user,

    title="Resume Tailored",

    message="AI generated a tailored resume."

)

    return render(
        request,
        "jobs/resume_tailor.html",
        {
            "analysis": analysis
        }
    )
from django.contrib.auth.decorators import login_required


@login_required
def cover_letter_view(request):

    import hashlib

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:
        return render(
            request,
            "jobs/cover_letter.html",
            {
                "cover_letter": "No resume uploaded."
            }
        )

    job_id = request.GET.get("job_id")

    if not job_id:
        return render(
            request,
            "jobs/cover_letter.html",
            {
                "cover_letter": "Job not found."
            }
        )

    try:
        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:
        return render(
            request,
            "jobs/cover_letter.html",
            {
                "cover_letter": "Invalid Job."
            }
        )

    # Generate hashes
    resume_hash = hashlib.sha256(
        resume.resume_text.encode()
    ).hexdigest()

    job_hash = hashlib.sha256(
        job.description.encode()
    ).hexdigest()

    # Check cache
    existing = CoverLetter.objects.filter(
        user=request.user,
        job=job,
        resume_hash=resume_hash,
        job_hash=job_hash,
    ).first()

    if existing:

        print("✅ Cover Letter Loaded From Cache")

        return render(
            request,
            "jobs/cover_letter.html",
            {
                "cover_letter": existing.content,
                "cached": True,
            }
        )

    print("🤖 Generating New Cover Letter...")

    letter = generate_cover_letter(
        resume.resume_text,
        job.description
    )

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

    Notification.objects.create(
        user=request.user,
        title="Cover Letter Ready",
        message="AI generated your cover letter."
    )

    if created:
        print("✅ Cover Letter Saved")
    else:
        print("✅ Cover Letter Updated")

    return render(
        request,
        "jobs/cover_letter.html",
        {
            "cover_letter": letter,
            "cached": False,
        }
    )
@login_required
def download_cover_letter_pdf(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    if not resume:

        return redirect(
            "real_jobs"
        )

    job_text = request.GET.get(
        "job_text",
        ""
    )

    cover_letter = generate_cover_letter(
        resume.resume_text,
        job_text
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="Cover_Letter.pdf"'
    )

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "CareerForge AI Cover Letter",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            cover_letter.replace(
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
def company_preparation(request):

    company = request.GET.get(
        "company",
        "Google"
    )

    preparation = CompanyPreparation.objects.filter(
        company__iexact=company
    ).first()

    if not preparation:

        prompt = f"""
Generate interview preparation for {company}.

Return ONLY in this format.

Overview:
...

Interview Rounds:
...

Required Skills:
...

Preparation Tips:
...
"""

        response = ask_llm(prompt)   # <-- use your existing LLM function

        sections = {}

        current = None

        for line in response.splitlines():

            line = line.strip()

            if line.startswith("Overview:"):
                current = "overview"
                sections[current] = line.replace("Overview:", "").strip()

            elif line.startswith("Interview Rounds:"):
                current = "interview_rounds"
                sections[current] = line.replace("Interview Rounds:", "").strip()

            elif line.startswith("Required Skills:"):
                current = "required_skills"
                sections[current] = line.replace("Required Skills:", "").strip()

            elif line.startswith("Preparation Tips:"):
                current = "preparation_tips"
                sections[current] = line.replace("Preparation Tips:", "").strip()

            elif current:
                sections[current] += "\n" + line

        preparation = CompanyPreparation.objects.create(

            company=company,

            overview=sections.get(
                "overview",
                ""
            ),

            interview_rounds=sections.get(
                "interview_rounds",
                ""
            ),

            required_skills=sections.get(
                "required_skills",
                ""
            ),

            preparation_tips=sections.get(
                "preparation_tips",
                ""
            ),

        )

    return render(

        request,

        "jobs/company_preparation.html",

        {

            "company": company,

            "data": preparation,

        }

    )

@login_required
def download_company_preparation_pdf(request):

    company = request.GET.get(
        "company",
        "Google"
    )

    preparation = CompanyPreparation.objects.filter(
        company__iexact=company
    ).first()

    if not preparation:
        return redirect("company_preparation")

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="{company}_Preparation.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"{company} Interview Preparation",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Company Overview</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            preparation.overview.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(
            "<b>Interview Rounds</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            preparation.interview_rounds.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(
            "<b>Required Skills</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            preparation.required_skills.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,12))

    story.append(
        Paragraph(
            "<b>Preparation Tips</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            preparation.preparation_tips.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return response

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from applications.models import Application
from notifications.models import Notification


@login_required
def apply_job(request):

    title = request.GET.get(
        "title",
        ""
    )

    company = request.GET.get(
        "company",
        ""
    )

    url = request.GET.get(
        "url",
        "#"
    )

    application, created = Application.objects.get_or_create(

        user=request.user,

        title=title,

        company=company,

        defaults={
            "url": url,
            "status": "Applied"
        }

    )

    if created:

        Notification.objects.create(

            user=request.user,

            title="Application Submitted",

            message=f"You applied for {title} at {company}."

        )

    return redirect(url)