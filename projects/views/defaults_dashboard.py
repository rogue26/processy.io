from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import Project

from workstreams.models import Workstream
from deliverables.models import Deliverable
from tasks.models import Task
from organizations.models import Organization


class DefaultsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "projects/defaults.html"
    login_url = "/"

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        project = Project.objects.filter(is_the_reference_project=True).first()

        organization = request.user.organization
        workstreams = list(Workstream.objects.filter(project__id=project.id))
        deliverables = list(Deliverable.objects.filter(project__id=project.id))
        tasks = list(Task.objects.filter(project__id=project.id))

        context['project'] = project
        context['organization'] = organization
        context['projects'] = Project.objects.filter(is_the_reference_project=False, created_by=request.user)
        context['workstreams'] = workstreams
        context['deliverables'] = deliverables
        context['tasks'] = tasks
        context['project_id'] = project.id

        return self.render_to_response(context)
