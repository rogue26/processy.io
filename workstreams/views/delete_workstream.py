from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalDeleteView

from ..models import Workstream


class DeleteWorkstream(BSModalDeleteView):
    model = Workstream
    template_name = 'workstreams/delete_workstream.html'
    success_message = 'Success: Workstream was deleted.'

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
