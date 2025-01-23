from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    AssignTaskToWorkerForm,
    AssignWorkersToTaskForm,
    PositionCreateUpdateForm,
    ProjectCreateUpdateForm,
    ProjectSearchForm,
    TagCreateUpdateForm,
    TagSearchForm,
    TaskCreateUpdateForm,
    TaskSearchForm,
    TaskTypeCreateUpdateForm,
    TaskTypeSearchForm,
    TeamCreateUpdateForm,
    TeamSearchForm,
    WorkerCreateForm,
    WorkerPasswordChangeForm,
    WorkerSearchForm,
    WorkerUpdateForm,
    WorkerTaskCompletionForm,
)

from manager.models import (
    Position,
    Project,
    Tag,
    Task,
    TaskType,
    Team,
    Worker,
    TaskAssignment,
)


def index(request: HttpRequest) -> HttpResponse:
    number_of_projects = Project.objects.count()
    number_of_teams = Team.objects.count()
    number_of_employees = Worker.objects.count()
    number_of_positions = Position.objects.count()
    number_of_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "number_of_projects": number_of_projects,
        "number_of_teams": number_of_teams,
        "number_of_employees": number_of_employees,
        "number_of_positions": number_of_positions,
        "number_of_tasks": number_of_tasks,
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

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = ProjectSearchForm(
            initial={
                "name": name
            },
        )

        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = "project"
    template_name = "manager/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
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
    template_name = "manager/project_create_update_form.html"
    success_url = reverse_lazy("manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectCreateUpdateForm
    template_name = "manager/project_create_update_form.html"
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

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TeamSearchForm(
            initial={
                "name": name
            }
        )

        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    context_object_name = "team"
    template_name = "manager/team_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team = self.get_object()
        context["team_workers"] = team.workers.values_list(
            "username",
            flat=True
        )

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateUpdateForm
    template_name = "manager/team_create_update_form.html"
    success_url = reverse_lazy("manager:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamCreateUpdateForm
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_create_update_form.html"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "positions"
    template_name = "manager/position_list.html"
    paginate_by = 5


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    context_object_name = "position"
    template_name = "manager/position_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PositionDetailView, self).get_context_data(**kwargs)
        position = self.get_object()
        context["position_workers"] = position.workers.values_list(
            "username",
            flat=True
        )

        return context


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateUpdateForm
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_create_update_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionCreateUpdateForm
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_create_update_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "manager/worker_list.html"
    queryset = Worker.objects.select_related("position")
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = WorkerSearchForm(
            initial={
                "username": username
            }
        )

        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "manager/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        worker = self.get_object()
        unique_projects = {
            project for team in self.object.teams.all()
            for project in team.projects.all()
        }
        context["worker_teams"] = worker.teams.values_list("name", flat=True)
        context["worker_tasks"] = worker.tasks.values_list("name", flat=True)
        context["task_assignments"] = TaskAssignment.objects.filter(
            worker=self.object
        )
        context["unique_projects"] = unique_projects

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_create_update_form.html"

    def form_valid(self, form):
        worker = form.save(commit=False)
        worker.position = form.cleaned_data["position"]
        worker.save()
        return redirect(self.success_url)


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_create_update_form.html"

    def form_valid(self, form):
        worker = form.save(commit=False)
        worker.position = form.cleaned_data["position"]
        worker.save()
        return redirect(self.success_url)


class WorkerChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = WorkerPasswordChangeForm
    success_url = reverse_lazy("manager:worker-detail")
    template_name = "manager/worker_change_password.html"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_delete.html"


class WorkerTaskCompletionView(LoginRequiredMixin, generic.UpdateView):
    model = TaskAssignment
    form_class = WorkerTaskCompletionForm
    template_name = "manager/worker_task_completion.html"
    success_url = reverse_lazy("manager:worker-list")

    def form_valid(self, form):
        form.instance.is_completed = True
        form.save()
        return redirect(self.success_url)


class AssignTaskToWorkerView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = AssignTaskToWorkerForm
    success_url = reverse_lazy("manager:worker-list")
    template_name = "manager/worker_assign_task.html"

    def form_valid(self, form):
        tasks = form.cleaned_data["tasks"]
        self.object.tasks.set(tasks)

        return super().form_valid(form)


class SignUpWorkerView(generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    success_url = reverse_lazy("login")
    template_name = "manager/worker_create_update_form.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "manager/tasks_list.html"
    queryset = Task.objects.select_related("task_type")
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        tasks = self.get_queryset()
        name = self.request.GET.get("name")

        workers = set()
        teams = set()

        for task in tasks:
            workers.update(task.assignees.values_list("username", flat=True))
            for project in task.projects.all():
                teams.update(project.teams.values_list("name", flat=True))

        context["task_teams"] = list(teams)
        context["task_workers"] = list(workers)
        context["search_form"] = TaskSearchForm(
            initial={
                "name": name,
            }
        )
        context["today"] = datetime.now()

        return context

    def get_queryset(self):
        queryset = Task.objects.annotate(
            priority_order=Case(
                When(priority="Urgent", then=Value(1)),
                When(priority="High", then=Value(2)),
                When(priority="Medium", then=Value(3)),
                When(priority="Low", then=Value(4)),
                output_field=IntegerField(),
            )
        ).order_by("priority_order")

        form = TaskSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("name"):
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task"
    template_name = "manager/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["task_workers"] = task.assignees.values_list(
            "username",
            flat=True
        )
        context["task_assignments"] = TaskAssignment.objects.filter(
            task=self.object
        )
        context["today"] = datetime.now()

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateUpdateForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_create_update_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateUpdateForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_create_update_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_delete.html"


class AssignWorkersToTaskView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = AssignWorkersToTaskForm
    template_name = "manager/assign_worker_to_task.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:task-detail",
            kwargs={"pk": self.object.pk}
        )


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_types"
    template_name = "manager/task_types.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TaskSearchForm(
            initial={
                "name": name,
            }
        )

        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateUpdateForm
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_create_update_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeCreateUpdateForm
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_create_update_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_delete.html"


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tags"
    template_name = "manager/tags_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TaskSearchForm(
            initial={
                "name": name,
            }
        )

        return context

    def get_queryset(self):
        queryset = Tag.objects.all()
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagCreateUpdateForm
    success_url = reverse_lazy("manager:tag-list")
    template_name = "manager/tag_create_update_form.html"


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagCreateUpdateForm
    success_url = reverse_lazy("manager:tag-list")
    template_name = "manager/tag_create_update_form.html"


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("manager:tag-list")
    template_name = "manager/tag_delete.html"
