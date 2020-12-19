from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from .forms import AddContentTypeForm, AddContentForm
from .models import Content, ContentType

class AddContentType(BSModalFormView):
    template_name = 'content/add_content_type.html'
    form_class = AddContentTypeForm

class AddContent(BSModalFormView):
    template_name = 'content/add_content.html'
    form_class = AddContentForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        # context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            pass
            # # get list of task types to add
            # task_types_to_add = self.request.POST.getlist('task_type')
            #
            # for task_type_num in task_types_to_add:
            #     task_type_name = TaskType.objects.get(id=int(task_type_num)).name
            #     new_task = Task.objects.create(name=task_type_name,
            #                                    description=task_type_name,
            #                                    project_id=self.kwargs['project_id'],
            #                                    category_id=int(task_type_num))
            #     new_task.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     if self.kwargs['project_id'] == 1:
    #         return reverse_lazy('defaults')
    #     else:
    #         return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})