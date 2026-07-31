from django.db import models
from django.contrib.auth.models import User
from pypdf import PdfReader

from .skill_extractor import extract_skills


class Skill(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    pdf = models.FileField(
        upload_to='resumes/'
    )

    resume_text = models.TextField(
        blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.pdf:

            reader = PdfReader(
                self.pdf.path
            )

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            Resume.objects.filter(
                pk=self.pk
            ).update(
                resume_text=text
            )

            skills_found = extract_skills(
                text
            )

            self.skills.clear()

            for skill_name in skills_found:

                skill, created = Skill.objects.get_or_create(
                    name=skill_name
                )

                self.skills.add(skill)

    def __str__(self):
        return self.name
    
class ResumeVersion(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title