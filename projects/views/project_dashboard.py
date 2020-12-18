import json
import datetime

from django.db.models import Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Project

from workstreams.models import Workstream
from deliverables.models import Deliverable
from tasks.models import Task
from organizations.models import Organization


def set_child_task_start_end(child_tasks):
    for task in child_tasks:

        if not task.prerequisite_tasks.exists():
            # todo: set this to something more sensible
            task.start_time = datetime.datetime.now()
        else:
            task.start_time = task.prerequisite_tasks.all().aggregate(Max('end_time'))['end_time__max']

        # set end time
        task.end_time = task.start_time + datetime.timedelta(days=float(task.baseline_fte_hours))
        task.save()

        # get child tasks and continue
        new_child_tasks = Task.objects.filter(prerequisite_tasks=task)

        if new_child_tasks:
            set_child_task_start_end(new_child_tasks)


def create_gantt_json(workstreams):
    gantt_dict = []
    for workstream in workstreams:

        for i, task in enumerate(Task.objects.filter(deliverable__workstream=workstream)):
            task_dict = \
                {
                    'id': i + 1,
                    'name': workstream.name,
                    'series':
                        [
                            {
                                'name': task.name,
                                'start': datetime.datetime(
                                    task.start_time.year,
                                    task.start_time.month,
                                    task.start_time.day).isoformat(),
                                'end': datetime.datetime(
                                    task.end_time.year,
                                    task.end_time.month,
                                    task.end_time.day).isoformat(),
                                'color': "#f0f0f0"
                            }
                        ]
                }

            gantt_dict.append(task_dict)
    return json.dumps(gantt_dict)



class ProjectsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "projects/project.html"
    login_url = '/'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        project = Project.objects.get(id=self.kwargs['project_id'])
        organization = request.user.organization

        workstreams = list(Workstream.objects.filter(project__id=self.kwargs['project_id']))
        deliverables = list(Deliverable.objects.filter(project__id=self.kwargs['project_id']))
        tasks = list(Task.objects.filter(project__id=self.kwargs['project_id']))

        all_project_tasks = Task.objects.filter(project=project)
        initial_tasks = all_project_tasks.filter(prerequisite_tasks__isnull=True)

        set_child_task_start_end(initial_tasks)

        context['project'] = project
        context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
        context['workstreams'] = workstreams
        context['deliverables'] = deliverables
        context['tasks'] = tasks
        context['project_id'] = self.kwargs['project_id']
        context['organization'] = organization
        context['gantt_json'] = create_gantt_json(workstreams)

        return self.render_to_response(context)
