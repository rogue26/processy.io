from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import TeamMember
from tasks.models import Task


class AddTeamMemberForm(BSModalModelForm):

    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = TeamMember
        fields = ['user', 'first_name', 'last_name', 'project_availability']
