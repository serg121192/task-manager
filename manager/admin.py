from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import (
    Task,
    TaskType,
    Worker,
    Position,
    Project,
    Team,
)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]
    list_filter = ["name", ]

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    search_fields = ["username", ]
    list_filter = ["username", ]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Add a position of an employee",
            {
                "fields": ("position",),
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info about employee's position, first name and last name",
            {
                "fields": (
                    "position",
                    "first_name",
                    "last_name",
                ),
            }
        ),
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]
    list_filter = ["name", ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    search_fields = ["name", ]
    list_filter = ["name", ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]
