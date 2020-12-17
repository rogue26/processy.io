from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalDeleteView

from ..models import Task


class DeleteTask(BSModalDeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_message = 'Success: Task was deleted.'

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
