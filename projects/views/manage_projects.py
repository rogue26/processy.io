from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
import json

from ..forms import ProjectForm
from ..models import Project


class ManageProjects(FormView):
    template_name = "projects/manage_projects.html"
    landing_template_name = "projects/index.html"
    form_class = ProjectForm
    success_url = "/"

    def get_form(self, form_class=None):
        form = super(ManageProjects, self).get_form()

        form.fields['client'].widget.attrs.update({'class': 'initial-hide'})

        organization = self.request.user.organization
        if organization is None:
            del form.fields['division']
        else:
            if not organization.division_set.all().exists():
                del form.fields['division']

        return form

    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return self.landing_template_name
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['organization'] = self.request.user.organization

            context['non_ref_projects'] = Project.objects.filter(is_the_reference_project=False,
                                                                 created_by=self.request.user)

            context['form_url'] = reverse_lazy('modals:add_organization')
            context['data_url'] = reverse_lazy('organizations:ajax_add_organization')
            context['modal_id'] = "#add-org-modal"
            context['data_element_id'] = "#addorg"

            context['has_org'] = json.dumps(self.request.user.organization is not None)
            context['user_declined_organization'] = json.dumps(self.request.user.declined_organization)

        return context

    def get_form_kwargs(self):
        # Sending user object to the form, to verify which fields to display/remove (depending on group)
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        if not self.request.is_ajax():
            # set created_by to be the current user
            form.instance.created_by = self.request.user

            # save the form data to model
            new_project = form.save()

            if 'save-project' in self.request.POST:
                return HttpResponseRedirect(super().get_success_url())
            elif 'add-workstreams' in self.request.POST:
                return redirect('projects:project', new_project.id)

        else:
            pass
