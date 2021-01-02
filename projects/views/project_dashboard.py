import json
from datetime import timedelta, datetime

from django.db.models import Max, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Project

from workstreams.models import Workstream
from deliverables.models import Deliverable
from tasks.models import Task
from content.models import Content
from teams.models import TeamMember


def create_gantt_json(project):
    project.setup_gantt()

    gantt_data = []
    for task in project.task_set.all():
        gantt_data.append(
            {
                'start': datetime(task.start.year, task.start.month, task.start.day).isoformat(),
                'end': datetime(task.end.year, task.end.month, task.end.day).isoformat(),
                'name': task.name,
                'id': "Task " + str(task.id),
                'progress': 0,
                'dependencies': ["Task " + str(parent_task.id) for parent_task in task.parent_tasks.all()]
            }
        )

    # todo:  do the sorting in python - can't do it in order_by because start is a method
    # sorted(Author.objects.all(), key=lambda a: a.full_name)

    return json.dumps(gantt_data, indent=4)


class ProjectsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "projects/project_dashboard.html"
    login_url = '/'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        project = Project.objects.get(id=self.kwargs['project_id'])

        workstreams = Workstream.objects.filter(project=project)
        deliverables = Deliverable.objects.filter(project=project)
        tasks = Task.objects.filter(project=project)
        team_members = TeamMember.objects.filter(project=project)

        context['project'] = project
        context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
        context['workstreams'] = workstreams
        context['deliverables'] = deliverables
        context['tasks'] = tasks
        context['organization'] = request.user.organization
        context['gantt_json'] = create_gantt_json(project)
        context['team_members'] = team_members

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
