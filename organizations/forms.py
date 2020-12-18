from django import forms


from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import Organization, Division


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'nickname', 'domain', 'letterhead', 'ppt_template']