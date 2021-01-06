from .forms import AddContentTypeForm, AddContentForm
from .models import Content, ContentType
from tasks.models import Task
from deliverables.models import Deliverable

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.db.models import Q

from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView

from organizations.forms import OrganizationForm, AddDivisionForm
from organizations.models import Organization

from projects.models import Project
from workstreams.models import Workstream


class AddContentType(BSModalFormView):
    template_name = 'content/add_content_type.html'
    form_class = AddContentTypeForm
    success_url = reverse_lazy('organization')

    def form_valid(self, form):
        if not self.request.is_ajax():

            # add organization to the contenttype object
            new_contenttype = form.save()
            new_contenttype.organization = self.request.user.organization
            new_contenttype.save()

        else:
            pass
        return HttpResponseRedirect(reverse_lazy('organization'))


class AddContent(BSModalFormView):
    template_name = 'content/add_content.html'
    form_class = AddContentForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(AddContent, self).get_form()

        form.fields['tasks'].queryset = \
            Task.objects \
                .filter(team_member__user=self.request.user, project__is_the_reference_project=False)

        form.fields['deliverables'].queryset = \
            Deliverable.objects.filter(Q(task__team_member__user=self.request.user))

        form.fields['workstreams'].queryset = \
            Workstream.objects.filter(Q(deliverable__task__team_member__user=self.request.user))

        return form

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():

            form.instance.uploaded_by = self.request.user
            new_content = form.save()

            # for each selected deliverable, find the deliverables it was copied from
            # and add those deliverables to the selected deliverables
            for workstream in new_content.workstreams.all():
                new_content.workstreams.add(workstream.copied_from)

            for deliverable in new_content.deliverables.all():
                new_content.deliverables.add(deliverable.copied_from)

            for task in new_content.tasks.all():
                new_content.tasks.add(task.copied_from)

            new_content.save()

        else:
            pass
        return HttpResponseRedirect("/content/")


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


def ajax_content_download(request):
    if request.method == 'GET':
        content = Content.objects.get(id=request.GET['content_id'])
        return HttpResponse(content.file.url)
    else:
        return HttpResponse("unsuccesful")
