from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SavedJob, Application
from .models import SavedJob
from activity.models import Activity
from notifications.models import Notification
@login_required
def save_job(request):

    title = request.GET.get("title")
    company = request.GET.get("company")
    url = request.GET.get("url")

    SavedJob.objects.create(
        user=request.user,
        title=title,
        company=company,
        url=url
    )
    Activity.objects.create(

    user=request.user,

    action="Saved Job",

    description=f"{title} at {company}"

)
    Notification.objects.create(

    user=request.user,

    title="Job Saved",

    message=f"{title} at {company} added to Saved Jobs."

)

    return redirect("saved_jobs")


@login_required
def saved_jobs(request):

    jobs = SavedJob.objects.filter(
        user=request.user
    ).order_by("-saved_at")

    return render(
        request,
        "applications/saved_jobs.html",
        {
            "jobs": jobs
        }
    )
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Application


@login_required
def apply_job(request):

    title = request.GET.get(
        "title",
        "Unknown"
    )

    company = request.GET.get(
        "company",
        "Unknown"
    )

    url = request.GET.get(
        "url",
        "#"
    )

    exists = Application.objects.filter(
        user=request.user,
        title=title,
        company=company
    ).exists()

    if not exists:

        Application.objects.create(
            user=request.user,
            title=title,
            company=company,
            status="Applied"
        )
        Activity.objects.create(

    user=request.user,

    action="Applied to Job",

    description=f"{title} at {company}"

)
        Notification.objects.create(

    user=request.user,

    title="Application Submitted",

    message=f"You applied for {title} at {company}."

)

    return redirect(url)
@login_required
def applications(request):

    apps = Application.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    return render(
        request,
        "applications/applications.html",
        {
            "applications": apps
        }
    )
@login_required
def delete_saved_job(
    request,
    id
):

    job = SavedJob.objects.filter(
        id=id,
        user=request.user
    ).first()

    if job:
        job.delete()

    return redirect(
        "saved_jobs"
    )
@login_required
def delete_application(
    request,
    id
):

    app = Application.objects.filter(
        id=id,
        user=request.user
    ).first()

    if app:
        app.delete()

    return redirect(
        "applications"
    )
@login_required
def update_application_status(request, id):

    app = Application.objects.filter(
        id=id,
        user=request.user
    ).first()

    if app:

        status = request.GET.get(
            "status",
            "Applied"
        )

        app.status = status

        app.save()

    return redirect(
        "applications"
    )