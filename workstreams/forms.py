from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import WorkstreamType, Workstream
from deliverables.models import Deliverable


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
    deliverables = forms.ModelMultipleChoiceField(
        queryset=Deliverable.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Workstream
        fields = ['category', 'name', 'description', 'objective', 'motivation', 'owner', 'deliverables']
