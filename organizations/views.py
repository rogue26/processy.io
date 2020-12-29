import json
import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView

from .forms import OrganizationForm, AddDivisionForm, OrganizationModalForm
from .models import Organization

from projects.models import Project


class AddDivision(BSModalCreateView):
    template_name = 'organizations/add_division.html'
    form_class = AddDivisionForm
    success_url = reverse_lazy('organization')

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
    success_url = reverse_lazy('manage_projects')


class AddOrganization(FormView):
    template_name = 'organizations/add_organization.html'
    form_class = OrganizationForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        # context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        org = form.save()

        user = self.request.user

        user.organization = Organization.objects.get(id=org.id)
        user.save()

        return HttpResponseRedirect('/')


class OrganizationDashboard(LoginRequiredMixin, TemplateView):
    template_name = "organizations/org_dashboard.html"
    login_url = '/'

    add_org_template_name = "organizations/add_organization.html"
    form_class = OrganizationForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.organization:
            return redirect(reverse_lazy('add_organization'))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        projects = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
        organization = request.user.organization

        context['organization'] = organization
        context['projects'] = projects

        return self.render_to_response(context)
