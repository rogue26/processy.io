
from organizations.models import Content


from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from projects.models import Project


class ContentDashboard(LoginRequiredMixin, TemplateView):
    template_name = "content/manage_content.html"
    login_url = '/'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = {}

        organization = request.user.organization
        content = Content.objects.filter(
            uploaded_by__organization=organization)
        projects = Project.objects.filter(is_the_reference_project=False, created_by=request.user)

        context['organization'] = organization
        context['content_items'] = content
        context['projects'] = projects

        return self.render_to_response(context)



