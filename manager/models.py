from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name}: {self.position})"


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    deadline = models.DateTimeField(
        default=datetime.now,
        null=False,
        blank=False
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=100,
        choices=(
            ("Urgent", "Urgent"),
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low"),
        ),
        null=False,
        blank=False
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=False
    )

    class Meta:
        ordering = ("priority", )

    def __str__(self):
        return f"{self.name} ({self.priority})"


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    teams = models.ManyToManyField(
        "Team",
        related_name="projects",
        blank=False
    )
    tasks = models.ManyToManyField(
        Task,
        related_name="projects",
        blank=False
    )

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=False
    )

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return f"{self.name} ({self.workers}): {self.description}"
