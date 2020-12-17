from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from ..forms import WorkstreamTypeForm
from ..models import WorkstreamType, Workstream

from projects.models import Project
from deliverables.models import Deliverable
from tasks.models import Task


class AddWorkstream(BSModalFormView):
    template_name = 'workstreams/add_workstream.html'
    form_class = WorkstreamTypeForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            # get list of workstream types to add
            workstream_types_to_add = self.request.POST.getlist('workstream_type')

            for workstream_type_num in workstream_types_to_add:
                workstream_type = WorkstreamType.objects.get(id=int(workstream_type_num))

                # if created for the reference project, then set is_the_default_workstream to True
                if self.kwargs['project_id'] == 1:
                    new_ws = Workstream.objects.create(name=workstream_type.name, description=workstream_type.name,
                                                       category_id=int(workstream_type_num),
                                                       project_id=self.kwargs['project_id'],
                                                       is_the_reference_workstream=True)
                    new_ws.save()
                else:
                    # copy the reference workstream for this workstream category
                    new_ws = Workstream.objects.filter(is_the_reference_workstream=True,
                                                       category=workstream_type).first()
                    old_deliverables = Deliverable.objects.filter(workstream_id=new_ws.id)
                    new_ws.pk = None
                    new_ws.project = Project.objects.get(id=self.kwargs['project_id'])
                    new_ws.is_the_reference_workstream = False
                    new_ws.save()

                    # now copy over all deliverables associated with the reference workstream
                    for old_deliverable in old_deliverables:
                        old_tasks = Task.objects.filter(deliverable_id=old_deliverable.id)
                        old_deliverable.pk = None
                        old_deliverable.project = Project.objects.get(id=self.kwargs['project_id'])
                        old_deliverable.is_the_reference_deliverable = False
                        old_deliverable.workstream = new_ws
                        old_deliverable.save()

                        # copy over all tasks associated with this deliverable in the reference configuration
                        for old_task in old_tasks:
                            old_task.pk = None
                            old_task.project = Project.objects.get(id=self.kwargs['project_id'])
                            old_task.is_the_reference_task = False
                            old_task.deliverable = old_deliverable
                            old_task.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['project_id'] == 1:
            return reverse_lazy('defaults')
        else:
            return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
