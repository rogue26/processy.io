import json
import datetime

from django.db.models import Max, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Project

from workstreams.models import Workstream
from deliverables.models import Deliverable
from tasks.models import Task
from content.models import Content
from organizations.models import Organization
from teams.models import TeamMember


# def set_child_task_start_end(child_tasks):
#     for task in child_tasks:
#
#         if not task.parent_tasks.exists():
#             # todo: set this to something more sensible
#             task.start = datetime.datetime.now()
#         else:
#             task.start = task.parent_tasks.all().aggregate(Max('end'))['end__max']
#
#         # set end time
#         task.end = task.start + datetime.timedelta(days=float(task.baseline_fte_days))
#         task.save()
#
#         # get child tasks and continue
#         new_child_tasks = Task.objects.filter(parent_tasks=task)
#
#         if new_child_tasks:
#             set_child_task_start_end(new_child_tasks)
#
#
# def create_gantt_json(workstreams):
#     gantt_dict = []
#     for workstream in workstreams:
#
#         for i, task in enumerate(Task.objects.filter(deliverable__workstream=workstream)):
#             task_dict = \
#                 {
#                     'id': i + 1,
#                     'name': workstream.name,
#                     'series':
#                         [
#                             {
#                                 'name': task.name,
#                                 'start': datetime.datetime(
#                                     task.start.year,
#                                     task.start.month,
#                                     task.start.day).isoformat(),
#                                 'end': datetime.datetime(
#                                     task.end.year,
#                                     task.end.month,
#                                     task.end.day).isoformat(),
#                                 'color': "#f0f0f0"
#                             }
#                         ]
#                 }
#
#             gantt_dict.append(task_dict)
#     return json.dumps(gantt_dict)


class ProjectsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "projects/project_dashboard.html"
    login_url = '/'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        project = Project.objects.get(id=self.kwargs['project_id'])

        project.setup_gantt()

        organization = request.user.organization

        workstreams = list(Workstream.objects.filter(project__id=self.kwargs['project_id']))
        deliverables = list(Deliverable.objects.filter(project__id=self.kwargs['project_id']))
        tasks = list(Task.objects.filter(project__id=self.kwargs['project_id']))

        all_project_tasks = Task.objects.filter(project=project)
        initial_tasks = all_project_tasks.filter(parent_tasks__isnull=True)

        # set_child_task_start_end(initial_tasks)

        context['project'] = project
        context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
        context['workstreams'] = workstreams
        context['deliverables'] = deliverables
        context['tasks'] = tasks
        context['project_id'] = self.kwargs['project_id']
        context['organization'] = organization
        # context['gantt_json'] = create_gantt_json(workstreams)
        context['team_members'] = TeamMember.objects.filter(project=project)

        # get content and related workstreams, deliverables, and tasks

        ## workstreams
        copied_workstreams = Workstream.objects.filter(copied_from_set__in=project.workstream_set.all())
        copied_deliverables = Deliverable.objects.filter(copied_from_set__in=project.deliverable_set.all())
        copied_tasks = Task.objects.filter(copied_from_set__in=project.task_set.all())

        content_items = Content.objects.filter(Q(workstreams__in=copied_workstreams) |
                                               Q(deliverables__in=copied_deliverables) |
                                               Q(tasks__in=copied_tasks))

        project_workstreams = \
            [project.workstream_set.all().prefetch_related('content_set').filter(content=_) for _ in content_items]

        project_deliverables = \
            [project.deliverable_set.all().prefetch_related('content_set').filter(content=_) for _ in content_items]

        project_tasks = \
            [project.task_set.all().prefetch_related('content_set').filter(content=_) for _ in content_items]

        content_data = zip(content_items, project_workstreams, project_deliverables, project_tasks)

        context['content_data'] = content_data
        return self.render_to_response(context)
