from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalDeleteView

from ..models import Deliverable


class DeleteDeliverable(BSModalDeleteView):
    model = Deliverable
    template_name = 'deliverables/delete_deliverable.html'
    success_message = 'Success: Deliverable was deleted.'

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('organization')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
