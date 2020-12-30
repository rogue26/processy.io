from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import TaskForm
from ..models import TaskType, Task, Resource, ComplexityDriver

from deliverables.models import Deliverable
from projects.models import Project


class ConfigureTask(BSModalFormView):
    template_name = 'tasks/configure_task.html'
    form_class = TaskForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ConfigureTask, self).get_form()
        form.fields['deliverable'].queryset = Deliverable.objects.filter(project_id=self.kwargs['project_id'])
        form.fields['prerequisite_tasks'].queryset = \
            Task.objects \
                .filter(project_id=self.kwargs['project_id']) \
                .exclude(id=self.kwargs['task_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_task = Task.objects.get(id=self.kwargs['task_id'])

        context["selected_prerequisite_tasks"] = \
            [_.pk for _ in current_task.prerequisite_tasks.all()]

        context["selected_required_resources"] = \
            [_.pk for _ in current_task.prerequisite_tasks.all()]

        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        current_task = Task.objects.get(id=self.kwargs['task_id'])

        initial = super().get_initial()

        initial['name'] = current_task.name
        initial['description'] = current_task.description
        initial['category'] = current_task.category

        initial['baseline_fte_days'] = current_task.baseline_fte_days
        initial['start_time'] = current_task.start_time
        initial['end_time'] = current_task.end_time
        initial['deliverable'] = current_task.deliverable
        initial['status'] = current_task.status
        initial['team_member'] = current_task.team_member

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template

        return initial

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        context['project_id'] = self.kwargs['project_id']
        context['task_id'] = self.kwargs['task_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            updated_form_data = self.request.POST

            task = Task.objects.get(id=self.kwargs['task_id'])

            task.name = updated_form_data.get('name')
            task.description = updated_form_data.get('description')
            task.category = TaskType.objects.get(id=updated_form_data.get('category'))
            task.baseline_fte_days = updated_form_data.get('baseline_fte_days')
            task.status = updated_form_data.get('status')

            try:
                task.team_member = updated_form_data.get('team_member')
            except ValueError:
                task.team_member = None

            task.project = Project.objects.get(id=self.kwargs['project_id'])
            task.deliverable = Deliverable.objects.get(id=updated_form_data.get('deliverable'))
            task.resources_required.set(Resource.objects.filter(pk__in=updated_form_data.getlist('resources_required')))

            task.prerequisite_tasks.set(Task.objects.filter(pk__in=updated_form_data.getlist('prerequisite_tasks')))

            task.complexity_drivers.set(
                ComplexityDriver.objects.filter(pk__in=updated_form_data.getlist('complexity_drivers')))

            task.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
