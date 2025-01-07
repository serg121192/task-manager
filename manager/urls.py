from django.urls import path

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
    WorkerListView,
    PositionDetailView,
    WorkerDetailView, TaskListView, TaskCreateView, TaskUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("", ProjectListView.as_view(), name="projects"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/update", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete", ProjectDeleteView.as_view(), name="project-delete"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete", TeamDeleteView.as_view(), name="team-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
]


app_name = "manager"
