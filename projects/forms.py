from django import forms
from projects.models import Client, Project
from bootstrap_modal_forms.forms import BSModalModelForm


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['timestamp']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['timestamp', 'workstream', 'is_the_reference_project', 'created_by']
        labels = {
            "name": "Project name"
        }
        # help_texts = {
        #     'client': "What is the name of the client?"
        # }

class AddProjectForm(BSModalModelForm):
    class Meta:
        model = Project
        exclude = ['timestamp', 'workstream', 'is_the_reference_project', 'created_by']
        labels = {
            "name": "Project name"
        }