from django.urls import path
from .views import (
    save_job,
    saved_jobs,
    apply_job,
    applications,
    delete_saved_job,
    delete_application,
    update_application_status
)

urlpatterns = [

    path(
        "save-job/",
        save_job,
        name="save_job"
    ),

    path(
        "saved-jobs/",
        saved_jobs,
        name="saved_jobs"
    ),
    path(
    "apply-job/",
    apply_job,
    name="apply_job"
),

    path(
    "applications/",
    applications,
    name="applications"
    ),
    
    path(
    "delete-saved-job/<int:id>/",
    delete_saved_job,
    name="delete_saved_job"
),
    path(
    "delete-application/<int:id>/",
    delete_application,
    name="delete_application"
),
    path(
    "update-application/<int:id>/",
    update_application_status,
    name="update_application_status"
),
]
