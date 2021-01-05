from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import DeliverableForm
from ..models import DeliverableType, Deliverable

from projects.models import Project
from workstreams.models import Workstream
from deliverables.models import Specification
from tasks.models import Task


class ConfigureDeliverable(BSModalFormView):
    template_name = 'deliverables/configure_deliverable.html'
    form_class = DeliverableForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ConfigureDeliverable, self).get_form()
        form.fields['workstream'].queryset = Workstream.objects.filter(project_id=self.kwargs['project_id'])
        form.fields['tasks'].queryset = Task.objects.filter(project_id=self.kwargs['project_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_deliverable = Deliverable.objects.get(id=self.kwargs['deliverable_id'])
        context["selected_tasks"] = \
            [_.pk for _ in Task.objects.filter(deliverable_id=self.kwargs['deliverable_id'])]
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        current_deliverable = Deliverable.objects.get(id=self.kwargs['deliverable_id'])

        initial = super().get_initial()

        initial['name'] = current_deliverable.name
        initial['category'] = current_deliverable.category
        initial['description'] = current_deliverable.description
        initial['scope'] = current_deliverable.scope
        initial['workstream'] = current_deliverable.workstream

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template

        return initial

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        context['project_id'] = self.kwargs['project_id']
        context['deliverable_id'] = self.kwargs['deliverable_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            updated_form_data = self.request.POST

            deliverable = Deliverable.objects.get(id=self.kwargs['deliverable_id'])

            deliverable.name = updated_form_data.get('name')
            deliverable.category = DeliverableType.objects.get(id=updated_form_data.get('category'))
            deliverable.description = updated_form_data.get('description')
            deliverable.scope = updated_form_data.get('scope')
            deliverable.workstream = Workstream.objects.get(id=updated_form_data.get('workstream'))

            specifications = Specification.objects.filter(pk__in=updated_form_data.getlist('specifications'))
            deliverable.specification_set.set(specifications)

            tasks = Task.objects.filter(pk__in=updated_form_data.getlist('tasks'))
            deliverable.task_set.set(tasks)

            deliverable.project = Project.objects.get(id=self.kwargs['project_id'])

            deliverable.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('organization')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
