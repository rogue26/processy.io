from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from .models import Organization, Division


class AddDivisionForm(BSModalModelForm):
    class Meta:
        model = Division
        fields = ['name']


class OrganizationModalForm(BSModalModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'nickname', 'domain', 'letterhead', 'ppt_template']
        labels = {
                    "domain": "Email domain",
                    "nickname": "Nickname (optional)",
                    "letterhead": "Letterhead (optional)",
                    "ppt_template": "Powerpoint template (optional)"
        }

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'nickname', 'domain', 'letterhead', 'ppt_template']
        labels = {
            "domain": "Email domain",
            "nickname": "Nickname (optional)",
            "letterhead": "Letterhead (optional)",
            "ppt_template": "Powerpoint template (optional)"
        }
