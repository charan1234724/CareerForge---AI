from django.db import models

class Application(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Interview", "Interview"),
        ("Selected", "Selected"),
        ("Rejected", "Rejected"),
    ]

    company = models.CharField(max_length=200)

    job_title = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    applied_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.company} - {self.job_title}"

from django.db import models
from django.contrib.auth.models import User


class PreparationTask(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company = models.CharField(
        max_length=100
    )

    task = models.CharField(
        max_length=200
    )

    completed = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.task
    
from django.db import models


from django.utils import timezone

class Job(models.Model):

    provider = models.CharField(
        max_length=50,
        default="Adzuna"
    )

    provider_job_id = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=300)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    description = models.TextField()

    required_skills = models.TextField(
        blank=True,
        default=""
    )

    salary_min = models.IntegerField(
        null=True,
        blank=True
    )

    salary_max = models.IntegerField(
        null=True,
        blank=True
    )

    url = models.URLField(
        max_length=1000,
        blank=True
    )

    source = models.CharField(
        max_length=50,
        default="Adzuna"
    )

    posted_date = models.DateField(
        null=True,
        blank=True
    )

    fetched_at = models.DateTimeField(
        auto_now=True
    )

    last_seen = models.DateTimeField(
        default=timezone.now
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
            models.Index(fields=["location"]),
            models.Index(fields=["provider_job_id"]),
        ]

    def __str__(self):
        return self.title
    
class SearchCache(models.Model):

    query = models.CharField(
        max_length=300,
        unique=True
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.query
    
from django.contrib.auth.models import User

class JobAlert(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    provider_job_id = models.CharField(
        max_length=200
    )

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "user",
            "provider_job_id",
        )

class CompanyPreparation(models.Model):

    company = models.CharField(
        max_length=200,
        unique=True
    )

    overview = models.TextField()

    interview_rounds = models.TextField()

    required_skills = models.TextField()

    preparation_tips = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company

import hashlib


class CoverLetter(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    resume_hash = models.CharField(
    max_length=64,
    blank=True,
    null=True
)

    job_hash = models.CharField(
    max_length=64,
    blank=True,
    null=True
)

    llm_model = models.CharField(
        max_length=100,
        default="deepseek/deepseek-chat"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            "user",
            "job",
        )