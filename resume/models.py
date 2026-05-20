from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    """
    One resume per user. Stores all resume data as database fields.
    The 'user' field links this resume to a specific registered user.
    OneToOneField means: one user → exactly one resume.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    linkedin = models.URLField(blank=True)          # blank=True = optional field
    github = models.URLField(blank=True)

    # Professional Summary (AI-generated)
    summary = models.TextField(blank=True)

    # Experience (stored as text, one job per line)
    experience = models.TextField(
        help_text="Each job on a new line. Format: JobTitle | Company | Year-Year | Description"
    )

    # Education
    education = models.TextField(
        help_text="Format: Degree | Institution | Year"
    )

    # Skills (comma-separated)
    skills = models.TextField(
        help_text="Separate skills with commas. E.g: Python, Django, SQL"
    )

    # Projects
    projects = models.TextField(
        blank=True,
        help_text="Format: ProjectName | Description | Tech Used"
    )

    # Certifications
    certifications = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated on every save

    def __str__(self):
        return f"Resume of {self.user.username}"

    def get_skills_list(self):
        """Returns skills as a Python list, split by commas."""
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_experience_list(self):
        """Returns experience as a list of dicts."""
        jobs = []
        for line in self.experience.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                jobs.append({
                    'title': parts[0],
                    'company': parts[1],
                    'period': parts[2],
                    'description': parts[3],
                })
        return jobs

    def get_education_list(self):
        """Returns education as a list of dicts."""
        edu_list = []
        for line in self.education.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                edu_list.append({
                    'degree': parts[0],
                    'institution': parts[1],
                    'year': parts[2],
                })
        return edu_list

    def get_projects_list(self):
        """Returns projects as a list of dicts."""
        projects = []
        for line in self.projects.strip().split('\n'):
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                projects.append({
                    'name': parts[0],
                    'description': parts[1],
                    'tech': parts[2],
                })
        return projects
# Create your models here.
