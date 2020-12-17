from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import TaskType, Task, ResourceType, ComplexityDriver


class AddTaskTypeForm(BSModalModelForm):
    class Meta:
        model = TaskType
        fields = ['name']


class TaskTypeForm(BSModalForm):
    task_type = forms.ModelMultipleChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        fields = ['task_type', 'clear']


class TaskForm(BSModalModelForm):
    resources_required = forms.ModelMultipleChoiceField(
        queryset=ResourceType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    prerequisite_tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    complexity_drivers = forms.ModelMultipleChoiceField(
        queryset=ComplexityDriver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Task
        fields = ['name', 'category', 'status', 'owner', 'deliverable', 'description', 'baseline_fte_hours',
                  'start_time', 'end_time', 'percent_complete', 'resources_required',
                  'prerequisite_tasks', 'complexity_drivers']
