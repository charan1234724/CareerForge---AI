from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from resumes.models import Resume
from applications.models import (
    SavedJob,
    Application
)

from ai_agents.resume_improver import (
    analyze_resume_improvement
)

from ai_agents.placement_tracker import (
    calculate_readiness
)


@login_required
def analytics_dashboard(request):

    users = User.objects.count()

    resumes = Resume.objects.count()

    saved_jobs = SavedJob.objects.count()

    applications = Application.objects.count()

    scores = []

    placement_scores = []

    total_skills = 0

    for resume in Resume.objects.all():

        result = analyze_resume_improvement(
            resume.resume_text
        )

        scores.append(
            result.get(
                "score",
                0
            )
        )

        total_skills += resume.skills.count()

        placement = calculate_readiness(
            resume,
            Application.objects.filter(
                user=resume.user
            ).count()
        )

        placement_scores.append(
            placement["score"]
        )

    avg_score = 0

    avg_placement = 0

    if scores:

        avg_score = round(
            sum(scores) /
            len(scores)
        )

    if placement_scores:

        avg_placement = round(
            sum(placement_scores) /
            len(placement_scores)
        )

    context = {

        "users": users,

        "resumes": resumes,

        "saved_jobs": saved_jobs,

        "applications": applications,

        "avg_score": avg_score,

        "avg_placement": avg_placement,

        "skills": total_skills,

        # Chart Data

        "chart_users": users,

        "chart_resumes": resumes,

        "chart_saved_jobs": saved_jobs,

        "chart_applications": applications,

        "chart_skills": total_skills,

    }

    return render(

        request,

        "analytics/dashboard.html",

        context

    )