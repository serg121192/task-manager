from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from manager.views import (
    index,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    PositionListView,
    PositionDetailView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    AssignWorkersToTaskView,
    WorkerChangePasswordView,
    SignUpWorkerView,
    AssignTaskToWorkerView,
    WorkerTaskCompletionView,
)
from task_manager.settings.base import *


urlpatterns = [
    path("", index, name="index"),
    path("", ProjectListView.as_view(), name="projects"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path(
        "teams/",
        TeamListView.as_view(),
        name="team-list"
    ),
    path(
        "teams/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "teams/create/",
        TeamCreateView.as_view(),
        name="team-create"
    ),
    path(
        "teams/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update"
    ),
    path(
        "teams/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/change_password/",
        WorkerChangePasswordView.as_view(),
        name="worker-change-password"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "workers/<int:pk>/assign_task/",
        AssignTaskToWorkerView.as_view(),
        name="worker-assign-task"
    ),
    path(
        "workers/<int:pk>/task/completion/",
        WorkerTaskCompletionView.as_view(),
        name="worker-task-completion"
    ),
    path(
        "setup_worker/",
        SignUpWorkerView.as_view(),
        name="signup-worker"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/assign_worker/",
        AssignWorkersToTaskView.as_view(),
        name="assign-workers-task"
    ),
    path(
        "task_types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "tags/",
        TagListView.as_view(),
        name="tag-list"
    ),
    path(
        "tags/create/",
        TagCreateView.as_view(),
        name="tag-create"
    ),
    path(
        "tags/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update"
    ),
    path(
        "tags/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete"
    ),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
] + static(STATIC_URL, document_root=STATIC_ROOT)


app_name = "manager"
