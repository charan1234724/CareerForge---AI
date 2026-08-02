from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from .views import update_ai_preferences
from django.contrib.auth.views import (

LoginView,

LogoutView,

)

from .views import (

signup,
delete_account,
profile,
settings_view,
download_my_data,
export_profile,
backup_data,
help_center,
contact_support,
faq,
report_bug,
)
from .dashboard import dashboard

urlpatterns=[

path(

"login/",

LoginView.as_view(

template_name=
"registration/login.html"

),

name="login"

),
path(
    "update-ai-preferences/",
    update_ai_preferences,
    name="update_ai_preferences",
),
path(
    "backup-data/",
    backup_data,
    name="backup_data",
),
path(
    "download-data/",
    download_my_data,
    name="download_data",
),
path(
    "contact-support/",
    contact_support,
    name="contact_support",
),
path(
    "report-bug/",
    report_bug,
    name="report_bug",
),
path(
    "export-profile/",
    export_profile,
    name="export_profile",
),
path(
    "help-center/",
    help_center,
    name="help_center"
),
path(
    "faq/",
    faq,
    name="faq"
),
path(

"logout/",

LogoutView.as_view(

next_page="login"

),

name="logout"

),

path(

"signup/",

signup,

name="signup"

),

path(

"dashboard/",

dashboard,

name="dashboard"

),

path(

"profile/",

profile,

name="profile"

),
path(

"settings/",

settings_view,

name="settings"

),
path(
    "password_reset/",
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.txt",
        html_email_template_name="registration/password_reset_email.html",
        success_url="/password_reset/done/",
    ),
    name="password_reset",
),
path(

    "delete/",

    delete_account,

    name="delete_account",

),
path(
    "password_reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ),
    name="password_reset_complete",
),

]