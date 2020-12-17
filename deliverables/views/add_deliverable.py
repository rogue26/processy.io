from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import DeliverableTypeForm
from ..models import DeliverableType, Deliverable


class AddDeliverable(BSModalFormView):
    template_name = 'deliverables/add_deliverable.html'
    form_class = DeliverableTypeForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            # get list of workstream types to add
            deliverable_types_to_add = self.request.POST.getlist('deliverable_type')

            for deliverable_type_num in deliverable_types_to_add:
                deliverable_type_name = DeliverableType.objects.get(id=int(deliverable_type_num)).name
                new_deliverable = Deliverable.objects.create(name=deliverable_type_name,
                                                             description=deliverable_type_name,
                                                             project_id=self.kwargs['project_id'],
                                                             category_id=int(deliverable_type_num))
                new_deliverable.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
