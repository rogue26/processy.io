from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm

from ..models import TeamMember
from projects.models import Task


class TaskModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.augmented_name


class TeamMemberForm(BSModalModelForm):
    tasks = TaskModelChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = TeamMember
        fields = ['user', 'first_name', 'last_name', 'project_availability']
