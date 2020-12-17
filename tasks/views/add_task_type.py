from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalCreateView

from ..forms import AddTaskTypeForm


class AddTaskType(BSModalCreateView):
    template_name = 'tasks/add_task_type.html'
    form_class = AddTaskTypeForm
    success_url = reverse_lazy('defaults')
