from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from projects.models import DeliverableType, Deliverable, ConditionType, SpecificationType
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
