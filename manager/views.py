from msilib.schema import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import ProjectCreateUpdateForm
from manager.models import Project, Team, Worker, Position


def index(request: HttpRequest) -> HttpResponse:
    number_of_projects = Project.objects.count()
    number_of_teams = Team.objects.count()
    number_of_employees = Worker.objects.count()
    number_of_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "number_of_projects": number_of_projects,
        "number_of_teams": number_of_teams,
        "number_of_employees": number_of_employees,
        "number_of_positions": number_of_positions,
        "num_visits": num_visits,
    }

    return render(
        request,
        "manager/index.html",
        context=context,
    )


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "projects"
    template_name = "manager/project_list.html"
    paginate_by = 5


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = "project"
    template_name = "manager/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        workers = set()
        for team in project.teams.all():
            workers.update(team.workers.values_list("username", flat=True))
        context["project_teams"] = project.teams.values_list("name", flat=True)
        context["project_tasks"] = project.tasks.values_list("name", flat=True)
        context["project_workers"] = list(workers)

        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateUpdateForm
    template_name = "manager/project_createupdate_form.html"
    success_url = reverse_lazy("manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreateUpdateForm
    template_name = "manager/project_createupdate_form.html"
    success_url = reverse_lazy("manager:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "manager/project_delete.html"
    success_url = reverse_lazy("manager:project-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "teams"
    template_name = "manager/teams_list.html"
    paginate_by = 5


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    context_object_name = "team"
    template_name = "manager/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context["team_workers"] = team.workers.values_list("username", flat=True)

        return context


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "positions"
    template_name = "manager/position_list.html"
    paginate_by = 10


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    context_object_name = "position"
    template_name = "manager/position_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = self.get_object()
        context["position_workers"] = position.workers.values_list("username", flat=True)

        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "manager/worker_list.html"
    queryset = Worker.objects.select_related("position")
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "manager/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        projects = set()
        context["worker_teams"] = worker.teams.values_list("name", flat=True)
        context["worker_tasks"] = worker.tasks.values_list("name", flat=True)
        for team in worker.teams.all():
            projects.update(team.projects.values_list("name", flat=True))
        context["worker_projects"] = list(projects)

        return context
