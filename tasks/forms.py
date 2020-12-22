from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import TaskType, Task, ResourceType, ComplexityDriver


# from django.forms import ModelChoiceField

class TaskModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.augmented_name


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

    prerequisite_tasks = TaskModelChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    complexity_drivers = forms.ModelMultipleChoiceField(
        queryset=ComplexityDriver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Task
        fields = ['name', 'category', 'status', 'team_member', 'deliverable', 'description', 'baseline_fte_hours',
                  'start_time', 'end_time', 'percent_complete', 'resources_required',
                  'prerequisite_tasks', 'complexity_drivers']
