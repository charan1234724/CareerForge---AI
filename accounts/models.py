from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    college = models.CharField(
        max_length=200,
        blank=True
    )

    branch = models.CharField(
        max_length=100,
        blank=True
    )

    graduation_year = models.CharField(
        max_length=20,
        blank=True
    )

    cgpa = models.DecimalField(
    max_digits=4,
    decimal_places=2,
    default=0,
    blank=True
)

    location = models.CharField(
        max_length=150,
        blank=True
    )

    dream_company = models.CharField(
        max_length=150,
        blank=True
    )

    dream_role = models.CharField(
        max_length=150,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    # =========================
    # Appearance
    # =========================

    THEME_CHOICES = [

    ("light", "Light"),

    ("dark", "Dark"),

]

    theme = models.CharField(

    max_length=10,

    choices=THEME_CHOICES,

    default="light"

)


# =========================
# Language
# =========================

    LANGUAGE_CHOICES = [

    ("en", "English"),

    ("te", "తెలుగు"),

    ("hi", "हिन्दी"),

]

    language = models.CharField(

    max_length=10,

    choices=LANGUAGE_CHOICES,

    default="en"

)


# =========================
# Timezone
# =========================

    TIMEZONE_CHOICES = [

    ("Asia/Kolkata", "India"),

    ("UTC", "UTC"),

]

    timezone = models.CharField(

    max_length=50,

    choices=TIMEZONE_CHOICES,

    default="Asia/Kolkata"

)


# =========================
# AI Preferences
# =========================

    ai_resume_analysis = models.BooleanField(

    default=True

)

    ai_career_recommendations = models.BooleanField(

    default=True

)

    ai_job_matching = models.BooleanField(

    default=True

)

    smart_notifications = models.BooleanField(

    default=True

)


# =========================
# Privacy
# =========================

    VISIBILITY_CHOICES = [

    ("private", "Private"),

    ("recruiters", "Recruiters Only"),

    ("public", "Public"),

]

    resume_visibility = models.CharField(

    max_length=20,

    choices=VISIBILITY_CHOICES,

    default="private"

)

    portfolio_visibility = models.CharField(

    max_length=20,

    choices=VISIBILITY_CHOICES,

    default="public"

)
    # Notification Preferences

    email_notifications = models.BooleanField(
    default=True
)

    job_alerts = models.BooleanField(
    default=True
)

    interview_reminders = models.BooleanField(
    default=True
)

    weekly_report = models.BooleanField(
    default=True
)

    def __str__(self):

        return self.user.username
    
class SupportTicket(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_resolved = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.user.username} - {self.subject}"
    
class BugReport(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    page = models.CharField(
        max_length=150,
        blank=True
    )

    screenshot = models.ImageField(
        upload_to="bug_reports/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_fixed = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.user.username} - {self.title}"