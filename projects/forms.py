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
        fields = ['internal', 'division', 'client', 'name', 'description', 'start_date']
        labels = {
            "name": "Project name",
            "internal": "Internal or external project?"
        }
        widgets = {
            'start_date': DateInput(),  # default date-format %m/%d/%Y will be used
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        # help_texts = {
        #     'internal': "Is this project internal or for an external client?"
        # }


class AddProjectForm(BSModalModelForm):
    class Meta:
        model = Project
        exclude = ['timestamp', 'workstream', 'is_the_reference_project', 'created_by']
        labels = {
            "name": "Project name"
        }
        widgets = {
            'start_date': DateInput(),  # default date-format %m/%d/%Y will be used
            # 'start_date': DatePickerInput(format='%Y-%m-%d'),  # specify date-frmat
        }
        # help_texts = {
        #     'client': "What is the name of the client?"
        # }
