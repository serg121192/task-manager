from django import forms

from manager.models import Team, Project, Task


class ProjectCreateUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = Project
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
