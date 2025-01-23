from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_type_name",
            ),
        ]

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
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"],
                name="unique_username_and_email",
            ),
        ]

    def __str__(self):
        if (self.first_name and self.last_name) and self.position:
            return (f"{self.username} ({self.first_name} {self.last_name}: "
                    f"{self.position})")
        elif self.first_name and self.last_name:
            return f"{self.username} ({self.first_name} {self.last_name})"
        elif self.position:
            return f"{self.username} ({self.position})"
        else:
            return f"{self.username}"


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_position_name",
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_tag_name",
            )
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    )
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    deadline = models.DateTimeField(
        default=datetime.now,
        null=False,
        blank=False
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TaskAssignment",
        related_name="tasks",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=True,
    )

    class Meta:
        ordering = ("-priority", )
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_task_name",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.priority})"


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    is_completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "worker"],
                name="unique_task_assignment",
            ),
        ]

    def update_completion(self):
        self.is_completed = True
        self.save()


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
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_project_name",
            )
        ]

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
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_team_name",
            )
        ]

    def __str__(self):
        if self.description:
            return f"{self.name}: {self.description}"

        return self.name
