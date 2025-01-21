from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from manager.models import (
    Team,
    Project,
    Task,
    Worker,
    TaskType,
    Tag,
    Position,
    TaskAssignment,
)


class ProjectCreateUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.prefetch_related("projects"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.prefetch_related("projects"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = "__all__"


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a project by name",
            }
        )
    )


class TeamCreateUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.prefetch_related("teams"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Team
        fields = "__all__"


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a team by name",
            }
        )
    )


class PositionCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"


class WorkerCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.prefetch_related("workers"),
        widget=forms.Select,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(UserChangeForm):
    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields.pop("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Worker.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already in use.")
        return username


class WorkerPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Worker
        fields = [
            "old_password",
            "new_password1",
            "new_password2",
        ]


class AssignTaskToWorkerForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Worker
        fields = []


class WorkerTaskCompletionForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = [
            "is_completed",
        ]
        widgets = {
            "is_completed": forms.CheckboxInput(),
        }


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a worker by username",
            }
        )
    )


class TaskCreateUpdateForm(forms.ModelForm):
    PRIORITY_CHOICES = (
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "datetime-local",
            }
        ),
        label="Deadline"
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.RadioSelect,
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.prefetch_related("tasks"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.prefetch_related("tasks"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.prefetch_related("tasks"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"


class AssignWorkersToTaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.prefetch_related("tasks"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "assignees",
        ]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a task by name",
            }
        )
    )


class TaskTypeCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a task by name",
            }
        )
    )


class TagCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a tag by name",
            }
        )
    )
