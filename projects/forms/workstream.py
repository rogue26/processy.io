from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from projects.models import WorkstreamType, Project, Workstream, Deliverable, Task
from projects.models import Deliverable


class AddWorkstreamTypeForm(BSModalModelForm):
    class Meta:
        model = WorkstreamType
        fields = ['name']


class WorkstreamTypeForm(BSModalForm):
    workstream_type = forms.ModelMultipleChoiceField(
        queryset=WorkstreamType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        fields = ['workstream_type', 'clear']


class WorkstreamForm(BSModalModelForm):
    test_attr = 3

    deliverables = forms.ModelMultipleChoiceField(
        queryset=Deliverable.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Workstream
        fields = ['category', 'name', 'description', 'objective', 'motivation', 'deliverables']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
