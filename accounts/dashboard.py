from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from resumes.models import Resume

from applications.models import (
    SavedJob,
    Application,
)

from ai_agents.resume_improver import (
    analyze_resume_improvement
)

from ai_agents.placement_tracker import (
    calculate_readiness
)
from activity.models import Activity
from ai_agents.dashboard_tasks import (
    generate_daily_tasks
)
from ai_agents.achievements import (
    calculate_achievements
)
from notifications.models import Notification
from datetime import datetime
from ai_agents.score_engine import (
    calculate_resume_scores
)
from accounts.models import StudentProfile
@login_required
def dashboard(request):

    resume = Resume.objects.filter(
        user=request.user
    ).last()

    scores = None

    if resume:

        scores = calculate_resume_scores(
        resume
    )
        ats_score = scores.ats_score
        resume_score = scores.resume_score

        career_score = scores.career_score

        health_score = scores.health_score

        profile_completion = scores.profile_completion
    saved_jobs_count = SavedJob.objects.filter(
        user=request.user
    ).count()

    applications_count = Application.objects.filter(
        user=request.user
    ).count()
    unread_notifications = Notification.objects.filter(
    user=request.user,
    is_read=False
).count()

    recent_applications = (
        Application.objects.filter(
            user=request.user
        ).order_by(
            "-applied_at"
        )[:5]
    )
    recent_activity = Activity.objects.filter(

    user=request.user

)[:6]

    skills_count = 0

    result = None

    placement = None

    placement_score = 0

    if scores:

        ats_score = scores.ats_score

        resume_score = scores.resume_score

        placement_score = scores.placement_score

        career_score = scores.career_score

        health_score = scores.health_score

        profile_completion = scores.profile_completion

        skill_match = scores.skill_match

    else:

        ats_score = 0

        resume_score = 0

        career_score = 0

        health_score = 0

        profile_completion = 0

        skill_match = 0
    top_career = "Not Available"
    daily_tasks = []
    achievements = []

    if resume:

        skills_count = (
            resume.skills.count()
        )

        result = analyze_resume_improvement(
            resume.resume_text
        )

        placement = calculate_readiness(
            resume,
            applications_count
        )
        daily_tasks = generate_daily_tasks(
    placement
)

        placement_score = placement.get(
            "score",
            0
        )
        achievements = calculate_achievements(

    resume,

    applications_count,

    placement_score,

    saved_jobs_count

)

        if result.get(
            "career_paths"
        ):

            top_career = (
                result["career_paths"][0]
            )

    current_hour = datetime.now().hour

    if current_hour < 12:

        greeting = "Good Morning ☀️"

    elif current_hour < 17:

        greeting = "Good Afternoon 🌤"

    else:

        greeting = "Good Evening 🌙"


    display_name = request.user.get_full_name()

    if not display_name:

        display_name = request.user.username
    goals = [

    {

"title":"Resume Uploaded",

"done": resume is not None

},

    {

"title":"Career Profile Completed",

"done": True

},

    {

"title":"Apply to 3 Jobs",

"done": applications_count >= 3

},

    {

"title":"Mock Interview",

"done": False

},

    {

"title":"ATS Above 90",

"done":

scores is not None

and

scores.ats_score >= 90

}

]

    completed = sum(

1 for g in goals if g["done"]

)

    goal_progress = int(

completed/len(goals)*100

)
    profile, created = StudentProfile.objects.get_or_create(
    user=request.user
)
    return render(
        request,
        "accounts/dashboard.html",
        {

            "resume": resume,
            "profile": profile,

            "saved_jobs":
            saved_jobs_count,

            "applications":
            applications_count,

            "recent_applications":
            recent_applications,

            "skills":
            skills_count,

            "result":
            result,

            "placement":placement,

            "top_career":top_career,
            "recent_activity":recent_activity,
            "daily_tasks": daily_tasks,
            "achievements": achievements,
            "unread_notifications": unread_notifications,
            "greeting": greeting,
            "display_name": display_name,
            "goals":goals,
            "goal_progress":goal_progress,
            "ats_score":scores.ats_score if scores else 0,
            "resume_score":scores.resume_score if scores else 0,
            "profile_completion":scores.profile_completion if scores else 0,
            "placement_score":scores.placement_score if scores else 0,
            "career_score":scores.career_score if scores else 0,
            "health_score":scores.health_score if scores else 0,

        }
    )