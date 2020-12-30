from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.urls import reverse_lazy
import json

from ..forms import ProjectForm
from ..models import Project

from workstreams.models import Workstream
from organizations.models import Organization


class ManageProjects(FormView):
    template_name = "projects/manage_projects.html"
    landing_template_name = "projects/index.html"
    form_class = ProjectForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ManageProjects, self).get_form()

        # print('test', self.request.user.organization.division_set.all().exists())
        # if not self.request.user.organization.division_set.all().exists():
        #     form.fields.remove('division')

        return form

    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return self.landing_template_name
        return super().get_template_names()

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        if self.request.user.is_authenticated:
            # create object of form
            form = ProjectForm(request.POST or None, request.FILES or None)

            organization = request.user.organization
            if organization is None:
                del form.fields['division']
            else:
                context['organization'] = organization
                if not organization.division_set.all().exists():
                    del form.fields['division']

            context['form'] = form
            context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)

            context['has_org'] = json.dumps(self.request.user.organization is not None)
            context['redirect_location'] = 'manage_projects'
            context['user_declined_organization'] = json.dumps(request.user.declined_organization)
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            # set created_by to be the current user
            form.instance.created_by = self.request.user

            # save the form data to model
            new_project = form.save()

            if 'save-project' in self.request.POST:
                return HttpResponseRedirect('/')
            elif 'add-workstreams' in self.request.POST:
                return HttpResponseRedirect('/project/' + str(new_project.pk))

        else:
            pass
