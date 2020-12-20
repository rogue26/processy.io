from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import ContentType, Content

from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from tasks.models import Task
from deliverables.models import Deliverable


class AugmentedModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.augmented_name


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

    class Meta:
        model = Content
        exclude = ['timestamp', 'tags', 'uploaded_by']
