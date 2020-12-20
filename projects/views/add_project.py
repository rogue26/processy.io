from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import AddProjectForm



class AddProject(BSModalFormView):
    template_name = 'projects/add_project.html'
    form_class = AddProjectForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        # context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            # set created_by to be the current user
            form.instance.created_by = self.request.user

            # save the form data to model
            new_project = form.save()
            self.kwargs['project_id'] = new_project.pk

            return HttpResponseRedirect('/project/' + str(new_project.pk))
        else:
            return HttpResponseRedirect('/')

