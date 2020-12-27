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
    # start_date = forms.DateField(
    #     widget=DatePickerInput,
    #     required=False)

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
