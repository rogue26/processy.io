from django import forms
from projects.models import Client, Project
from bootstrap_modal_forms.forms import BSModalModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['timestamp']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'division', 'internal', 'client', 'description', 'start_date']
        labels = {
            "name": "Project name",
            "internal": "Internal or external client?"
        }
        widgets = {
            'start_date': DateInput(),  # default date-format %m/%d/%Y will be used
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            self.instance.created_by = self.request.user
            self.instance.organization = self.request.user.organization
        return super().save(commit=commit)


class ProjectModalForm(BSModalModelForm):
    class Meta:
        model = Project
        fields = ['name', 'division', 'internal', 'client', 'description', 'start_date']
        labels = {
            "name": "Project name",
            "internal": "Internal or external client?"
        }
        widgets = {
            'start_date': DateInput(),  # default date-format %m/%d/%Y will be used
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        if commit:
            self.instance.created_by = self.request.user
            self.instance.organization = self.request.user.organization
        return super().save(commit=commit)
