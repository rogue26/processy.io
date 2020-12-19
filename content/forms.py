from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import ContentType, Content


class AddContentTypeForm(BSModalModelForm):
    class Meta:
        model = ContentType
        fields = ['name']


class AddContentForm(BSModalModelForm):
    class Meta:
        model = Content
        exclude = ['timestamp', 'tags', 'uploaded_by']
