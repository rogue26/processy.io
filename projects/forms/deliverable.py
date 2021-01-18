from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from projects.models import Workstream, DeliverableType, Deliverable, ConditionType, SpecificationType
from projects.models import Task


class AddDeliverableTypeForm(BSModalModelForm):
    class Meta:
        model = DeliverableType
        fields = ['name']


class DeliverableTypeForm(BSModalModelForm):
    deliverable_type = forms.ModelMultipleChoiceField(
        queryset=DeliverableType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = Deliverable
        fields = ['deliverable_type']


class DeliverableForm(BSModalModelForm):
    # conditions = forms.ModelMultipleChoiceField(
    #     queryset=ConditionType.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False)
    #
    # specifications = forms.ModelMultipleChoiceField(
    #     queryset=SpecificationType.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False)

    tasks = forms.ModelMultipleChoiceField(
        label='Supporting tasks',
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    # workstreams = forms.ModelChoiceField(
    #     label='Workstream',
    #     queryset=Workstream.objects.all(),
    #     widget=forms.Select,
    #     required=False)

    class Meta:
        model = Deliverable
        fields = ['category', 'name', 'description', 'workstream', 'tasks']
        labels = {
            "category": "Deliverable type",
            "name": "Deliverable name",
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
