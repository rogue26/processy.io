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

    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return self.landing_template_name
        return super().get_template_names()

    # def dispatch(self, request, *args, **kwargs):
    #     # check if the user already has an organization assigned to them.
    #     # if not, redirect them to the add_organization_modal to provide one.
    #     if request.user.organization:
    #         print('user has organization')
    #         return super(ManageProjects, self).dispatch(request, *args, **kwargs)
    #     else:
    #         print('no organization')
    #         return HttpResponseRedirect(reverse_lazy('add_organization_modal'))

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        if self.request.user.is_authenticated:
            # create object of form
            form = ProjectForm(request.POST or None, request.FILES or None)

            organization = request.user.organization
            context['form'] = form
            context['organization'] = organization
            context['workstreams'] = Workstream.objects.all()
            context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
            context['workstream_columns'] = range(2)
            context['has_org'] = json.dumps(self.request.user.organization is not None)

            print('test', json.dumps(self.request.user.organization is not None))
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
