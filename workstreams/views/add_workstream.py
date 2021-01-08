import traceback

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
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':

            # get list of workstream types to add
            workstream_types_to_add = self.request.POST.getlist('workstream_type')

            project = Project.objects.get(id=self.kwargs['project_id'])
            for workstream_type_num in workstream_types_to_add:
                workstream_type = WorkstreamType.objects.get(id=int(workstream_type_num))

                # if created for the reference project, then set is_the_default_workstream to True
                if project.is_the_reference_project:
                    new_ws = Workstream.objects.create(name=workstream_type.name, description=workstream_type.name,
                                                       category_id=int(workstream_type_num),
                                                       project_id=self.kwargs['project_id'],
                                                       is_the_reference_workstream=True)
                    new_ws.save()
                else:
                    # attempt to copy the reference workstream for this workstream category
                    #
                    try:
                        new_ws = Workstream.objects.filter(is_the_reference_workstream=True,
                                                           category=workstream_type).first()
                        reference_ws_id = new_ws.id
                        old_deliverables = Deliverable.objects.filter(workstream_id=new_ws.id)

                        new_ws.pk = None
                        new_ws.project = Project.objects.get(id=self.kwargs['project_id'])
                        new_ws.is_the_reference_workstream = False
                        new_ws.save()

                        new_ws.copied_from_id = reference_ws_id
                        new_ws.save()

                        # now copy over all deliverables associated with the reference workstream
                        for old_deliverable in old_deliverables:
                            old_tasks = Task.objects.filter(deliverable_id=old_deliverable.id)
                            reference_deliverable_id = old_deliverable.id
                            old_deliverable.pk = None
                            old_deliverable.project = Project.objects.get(id=self.kwargs['project_id'])
                            old_deliverable.is_the_reference_deliverable = False
                            old_deliverable.workstream = new_ws
                            old_deliverable.save()
                            old_deliverable.copied_from_id = reference_deliverable_id
                            old_deliverable.save()

                            # copy over all tasks associated with this deliverable in the reference configuration
                            for old_task in old_tasks:
                                reference_task_id = old_task.id
                                old_task.pk = None
                                old_task.project = Project.objects.get(id=self.kwargs['project_id'])
                                old_task.is_the_reference_task = False
                                old_task.deliverable = old_deliverable
                                old_task.save()
                                old_task.copied_from_id = reference_task_id
                                old_task.save()
                    except:
                        new_ws = Workstream.objects.create(name=workstream_type.name, description=workstream_type.name,
                                                           category_id=int(workstream_type_num),
                                                           project_id=self.kwargs['project_id'],
                                                           is_the_reference_workstream=False)
                        new_ws.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        if project.is_the_reference_project:
            return reverse_lazy('organizations:organization')
        else:
            return reverse_lazy('projects:project', kwargs={'project_id': self.kwargs['project_id']})
