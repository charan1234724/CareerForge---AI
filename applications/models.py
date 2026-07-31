from django.db import models
from django.contrib.auth.models import User


class SavedJob(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=300
    )

    company = models.CharField(
        max_length=300
    )

    url = models.URLField()

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = [
        ("Applied", "🟡 Applied"),
        ("Shortlisted", "🔵 Shortlisted"),
        ("Interview", "🟠 Interview Scheduled"),
        ("Offer", "🟢 Offer Received"),
        ("Rejected", "🔴 Rejected"),
        ("Withdrawn", "⚪ Withdrawn"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=300
    )

    company = models.CharField(
        max_length=300
    )

    url = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - {self.company}"