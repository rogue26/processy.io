from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import ContentType, Content

from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from tasks.models import Task
from deliverables.models import Deliverable
from workstreams.models import Workstream


class AugmentedModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.augmented_name2


class AddContentTypeForm(BSModalModelForm):
    class Meta:
        model = ContentType
        fields = ['name']


class AddContentForm(BSModalModelForm):
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
