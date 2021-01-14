from django import forms

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm

from projects.models import Project
from organizations.models import Organization, Division


class DivisionForm(BSModalModelForm):
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

    def save(self, commit=True):
        if commit:
            self.request.user.organization = self.instance
            self.request.user.save()

            pre_existing_ref_projects = Project.objects.filter(is_the_reference_project=True,
                                                               created_by=self.request.user)

            if not pre_existing_ref_projects.exists():
                ref_project = Project(name="Reference project",
                                      description="Placeholder project for holding an "
                                                  "organization's default workstreams.",
                                      is_the_reference_project=True)
                ref_project.save()

                ref_project.organization = self.instance
                ref_project.save()
            else:
                # if a user has a "personal" reference project and they create an organization, that reference project
                # will be associated with the organization. At the moment, processy doesn't allow for both a personal
                # reference project and an organization reference project under the same account. This is probably the
                # correct behavior, but this can be revisited later.
                ref_project = pre_existing_ref_projects.first()
                ref_project.organization = self.instance

        return super().save(commit=commit)


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
