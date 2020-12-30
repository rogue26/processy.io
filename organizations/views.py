import json

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from projects.models import Project

from .forms import OrganizationForm, AddDivisionForm, OrganizationModalForm

from workstreams.models import Workstream
from deliverables.models import Deliverable
from tasks.models import Task


class AddDivision(BSModalCreateView):
    template_name = 'organizations/add_division.html'
    form_class = AddDivisionForm

    # success_url = reverse_lazy('organization')

    def form_valid(self, form):

        if not self.request.is_ajax():
            form.instance.organization = self.request.user.organization
            form.save()
        else:
            pass
        return HttpResponseRedirect(reverse_lazy('organization'))


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
                # and organization reference project under the same account. This is probably the correct behavior,
                # but this can be revisted later.

                ref_project = pre_existing_ref_projects.first()
                ref_project.organization = org
                ref_project.client = org.name

        else:
            pass

        return HttpResponseRedirect(self.get_success_url())


class OrganizationDashboard(LoginRequiredMixin, TemplateView):
    template_name = "organizations/org_dashboard.html"
    login_url = '/'

    # add_org_template_name = "organizations/add_organization.html"
    form_class = OrganizationForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        if request.user.organization:
            projects = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
            organization = request.user.organization

            context['organization'] = organization
            context['projects'] = projects

        context['has_org'] = json.dumps(request.user.organization is not None)
        context['redirect_location'] = 'organization'

        return self.render_to_response(context)


class DefaultsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "organizations/defaults.html"
    login_url = "/"

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        ref_projects = Project.objects.filter(is_the_reference_project=True, organization=request.user.organization)

        if ref_projects.exists():
            ref_project = ref_projects.first()
            context['ref_project'] = ref_project
            context['workstreams'] = Workstream.objects.filter(project__id=ref_project.id)
            context['deliverables'] = Deliverable.objects.filter(project__id=ref_project.id)
            context['tasks'] = Task.objects.filter(project__id=ref_project.id)

        context['has_org'] = json.dumps(request.user.organization is not None)
        context['redirect_location'] = 'defaults'

        return self.render_to_response(context)


def update_declined_organization(request):
    if request.method == 'POST':
        user = request.user
        user.declined_organization = True
        user.save()

        ref_project = Project()
        ref_project.name = "Reference project"
        ref_project.description = "Placeholder project for holding an organization's default workstreams."
        ref_project.client = user.email
        ref_project.is_the_reference_project = True

        ref_project.save()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)
