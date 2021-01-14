from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm

from organizations.models import ContentType, Content
from projects.models import Task
from projects.models import Deliverable
from projects.models import Workstream


class AugmentedModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.augmented_name2


class ContentTypeForm(BSModalModelForm):
    class Meta:
        model = ContentType
        fields = ['name']


class ContentForm(BSModalModelForm):
    tasks = AugmentedModelChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    deliverables = AugmentedModelChoiceField(
        queryset=Deliverable.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    workstreams = AugmentedModelChoiceField(
        queryset=Workstream.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Content
        exclude = ['timestamp', 'tags', 'uploaded_by']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            self.instance.uploaded_by = self.request.user

            # for each selected project component, find the components from which it was copied
            # and add those deliverables to the selected deliverables
            for workstream in self.instance.workstreams.all():
                self.instance.workstreams.add(workstream.copied_from)

            for deliverable in self.instance.deliverables.all():
                self.instance.deliverables.add(deliverable.copied_from)

            for task in self.instance.tasks.all():
                self.instance.tasks.add(task.copied_from)

        return super().save(commit=commit)
