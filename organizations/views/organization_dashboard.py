import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from ..forms import OrganizationForm

from projects.models import Project
from projects.models import Workstream, WorkstreamType
from projects.models import Deliverable, DeliverableType
from projects.models import Task, TaskType
from organizations.models import ContentType


class OrganizationDashboard(LoginRequiredMixin, TemplateView):
    template_name = "organizations/organization_dashboard.html"
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
            context['workstream_types'] = WorkstreamType.objects.filter(organization=organization)
            context['deliverable_types'] = DeliverableType.objects.filter(organization=organization)
            context['task_types'] = TaskType.objects.filter(organization=organization)
            context['content_types'] = ContentType.objects.filter(organization=organization)
            context['org_form'] = OrganizationForm()
            context['org_form'].fields['name'].initial = organization.name
            context['org_form'].fields['nickname'].initial = organization.nickname
            context['org_form'].fields['domain'].initial = organization.domain

            non_ref_projects = Project.objects.filter(is_the_reference_project=False,
                                                      organization=organization)
            context['non_ref_projects'] = non_ref_projects

        context['deliverable_type_form_url'] = reverse_lazy('modals:add_deliverable_type')
        context['deliverable_type_data_url'] = reverse_lazy('organizations:ajax_add_deliverable_type')
        context['deliverable_type_modal_id'] = "#create-modal"
        context['deliverable_type_data_element_id'] = "#addorg"

        context['form_url'] = reverse_lazy('modals:add_organization')
        context['data_url'] = reverse_lazy('organizations:ajax_add_organization')
        context['modal_id'] = "#add-org-modal"
        context['data_element_id'] = "#addorg"
        context['has_org'] = json.dumps(self.request.user.organization is not None)

        return context
