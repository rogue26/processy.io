from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import WorkstreamForm
from ..models import WorkstreamType, Workstream

from deliverables.models import Deliverable


class ConfigureWorkstream(BSModalFormView):
    template_name = 'workstreams/configure_workstream.html'
    form_class = WorkstreamForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ConfigureWorkstream, self).get_form()
        form.fields['deliverables'].queryset = Deliverable.objects.filter(project_id=self.kwargs['project_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_ws = Workstream.objects.get(id=self.kwargs['workstream_id'])
        context["selected_deliverables"] = \
            [_.pk for _ in Deliverable.objects.filter(workstream_id=self.kwargs['workstream_id'])]
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        current_ws = Workstream.objects.get(id=self.kwargs['workstream_id'])

        initial = super().get_initial()

        initial['name'] = current_ws.name
        initial['category'] = current_ws.category
        initial['description'] = current_ws.description
        initial['objective'] = current_ws.objective
        initial['motivation'] = current_ws.motivation
        initial['owner'] = current_ws.owner

        return initial

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        context['project_id'] = self.kwargs['project_id']
        context['workstream_id'] = self.kwargs['workstream_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            updated_form_data = self.request.POST

            ws = Workstream.objects.get(id=self.kwargs['workstream_id'])

            ws.category = WorkstreamType.objects.get(id=updated_form_data.get('category'))
            ws.name = updated_form_data.get('name')
            ws.description = updated_form_data.get('description')
            ws.objective = updated_form_data.get('objective')
            ws.motivation = updated_form_data.get('motivation')
            ws.owner = updated_form_data.get('owner')

            deliverables = Deliverable.objects.filter(pk__in=updated_form_data.getlist('deliverables'))
            ws.deliverable_set.set(deliverables)

            ws.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
