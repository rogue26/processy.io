import json

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from projects.models import Project

from .forms import OrganizationForm, AddDivisionForm, OrganizationModalForm

from workstreams.models import Workstream
from deliverables.models import Deliverable, DeliverableType
from tasks.models import Task
from content.models import ContentType


class AddDivision(BSModalCreateView):
    template_name = 'organizations/add_division.html'
    form_class = AddDivisionForm

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
                # reference project and an organization reference project under the same account. This is probably the
                # correct behavior, but this can be revisited later.

                ref_project = pre_existing_ref_projects.first()
                ref_project.organization = org
                ref_project.client = org.name

        else:
            pass

        return HttpResponseRedirect(self.get_success_url())


class OrganizationDashboard(LoginRequiredMixin, TemplateView):
    template_name = "organizations/org_dashboard.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(OrganizationDashboard, self).get_context_data(**kwargs)

        ref_projects = Project.objects.filter(is_the_reference_project=True,
                                              organization=self.request.user.organization)
        if ref_projects.exists():
            ref_project = ref_projects.first()
            context['project'] = ref_project
            context['workstreams'] = Workstream.objects.filter(project__id=ref_project.id)
            context['deliverables'] = Deliverable.objects.filter(project__id=ref_project.id)
            context['tasks'] = Task.objects.filter(project__id=ref_project.id)

        if self.request.user.organization:
            organization = self.request.user.organization
            context['organization'] = organization
            context['deliverable_types'] = DeliverableType.objects.filter(organization=organization)
            context['content_types'] = ContentType.objects.filter(organization=organization)
            context['org_form'] = OrganizationForm()
            context['org_form'].fields['name'].initial = organization.name
            context['org_form'].fields['nickname'].initial = organization.nickname
            context['org_form'].fields['domain'].initial = organization.domain

            non_ref_projects = Project.objects.filter(is_the_reference_project=False,
                                                      organization=organization)
            context['non_ref_projects'] = non_ref_projects


        context['has_org'] = json.dumps(self.request.user.organization is not None)
        context['redirect_location'] = 'organization'
        return context


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
