from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from ..models import Project

from projects.models import Workstream
from projects.models import Deliverable
from projects.models import Task
from organizations.models import Content
from projects.models import TeamMember


class ProjectsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "projects/project_dashboard.html"
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.get(id=self.kwargs['project_id'])

        context['project'] = project
        context['non_ref_projects'] = Project.objects.filter(is_the_reference_project=False,
                                                             created_by=self.request.user)
        context['workstreams'] = Workstream.objects.filter(project=project)
        context['deliverables'] = Deliverable.objects.filter(project=project)
        context['tasks'] = Task.objects.filter(project=project)
        context['organization'] = self.request.user.organization
        context['team_members'] = TeamMember.objects.filter(project=project)

        context['workstream_form_url'] = reverse_lazy('modals:add_workstream', kwargs={'project_id': project.id})
        context['workstream_data_url'] = reverse_lazy('projects:update_workstreams_table', kwargs={'project_id': project.id})
        context['workstream_data_element_id'] = "#workstreams-table"
        context['deliverable_form_url'] = reverse_lazy('modals:add_deliverable', kwargs={'project_id': project.id})
        context['deliverable_data_url'] = reverse_lazy('projects:update_deliverables_table', kwargs={'project_id': project.id})
        context['deliverable_data_element_id'] = "#deliverables-table"
        context['task_form_url'] = reverse_lazy('modals:add_task', kwargs={'project_id': project.id})
        context['task_data_url'] = reverse_lazy('projects:update_tasks_table', kwargs={'project_id': project.id})
        context['task_data_element_id'] = "#tasks-table"

        context['modal_id'] = "#create-modal"

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

        return context
