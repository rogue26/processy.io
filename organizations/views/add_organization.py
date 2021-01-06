from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from projects.models import Project

from ..forms import OrganizationModalForm


class AddOrganizationModal(BSModalCreateView):
    template_name = 'organizations/add_organization_modal.html'
    form_class = OrganizationModalForm

    def get_success_url(self):
        try:
            return reverse_lazy(self.kwargs['redirect_location'])
        except:
            return reverse_lazy('manage_projects')

    def form_valid(self, form):

        if not self.request.is_ajax():

            org = form.save()

            user = self.request.user
            user.organization = org
            user.save()

            pre_existing_ref_projects = Project.objects.filter(is_the_reference_project=True, created_by=user)

            if not pre_existing_ref_projects.exists():
                ref_project = Project()
                ref_project.name = "Reference project"
                ref_project.description = "Placeholder project for holding an organization's default workstreams."
                ref_project.client = org.name
                ref_project.is_the_reference_project = True

                ref_project.save()
            else:
                # if a user has a "personal" reference project and they create an organization, that reference project
                # will be associated with the organization. At the moment, processy doesn't allow for both a personal
                # reference project and an organization reference project under the same account. This is probably the
                # correct behavior, but this can be revisited later.

                ref_project = pre_existing_ref_projects.first()
                ref_project.organization = org
                ref_project.client = org.name

        else:
            pass

        return HttpResponseRedirect(self.get_success_url())
