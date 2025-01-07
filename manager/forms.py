from django import forms

from manager.models import Team, Project, Task, Worker


class ProjectCreateUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.prefetch_related(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.prefetch_related(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = "__all__"


class TeamCreateUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.prefetch_related(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Team
        fields = "__all__"


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
        queryset=Worker.objects.prefetch_related(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
