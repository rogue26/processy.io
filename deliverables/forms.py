from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import DeliverableType, Deliverable, ConditionType, SpecificationType
from tasks.models import Task


class AddDeliverableTypeForm(BSModalModelForm):
    class Meta:
        model = DeliverableType
        fields = ['name']


class DeliverableTypeForm(BSModalForm):
    deliverable_type = forms.ModelMultipleChoiceField(
        queryset=DeliverableType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        fields = ['deliverable_type', 'clear']


class DeliverableForm(BSModalModelForm):
    conditions = forms.ModelMultipleChoiceField(
        queryset=ConditionType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    specifications = forms.ModelMultipleChoiceField(
        queryset=SpecificationType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Deliverable
        fields = ['name', 'category', 'workstream', 'scope', 'conditions', 'specifications', 'tasks']
