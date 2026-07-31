from django.db import models
from django.contrib.auth.models import User


class JobPreference(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    preferred_role = models.CharField(
        max_length=200,
        default="Python Developer"
    )

    preferred_location = models.CharField(
        max_length=200,
        default="India"
    )

    remote = models.BooleanField(
        default=False
    )

    internship = models.BooleanField(
        default=False
    )

    fresher = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.user.username