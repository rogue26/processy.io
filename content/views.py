from .forms import AddContentTypeForm, AddContentForm
from .models import Content, ContentType
from tasks.models import Task
from deliverables.models import Deliverable

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView

from organizations.forms import OrganizationForm, AddDivisionForm
from organizations.models import Organization

from projects.models import Project


class AddContentType(BSModalFormView):
    template_name = 'content/add_content_type.html'
    form_class = AddContentTypeForm


class AddContent(BSModalFormView):
    template_name = 'content/add_content.html'
    form_class = AddContentForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(AddContent, self).get_form()

        form.fields['tasks'].queryset = \
            Task.objects.filter(
                project__created_by=self.request.user,  # todo - replace with projects user was involved with
                project_id__gt=1
            )

        form.fields['deliverables'].queryset = \
            Deliverable.objects.filter(
                project__created_by=self.request.user,  # todo - replace with projects user was involved with
                project_id__gt=1
            )

        return form

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        context = self.get_context_data()
        # context['project_id'] = self.kwargs['project_id']
        return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            form.instance.uploaded_by = self.request.user
            form.save()

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


        context['organization'] = organization
        context['content_items'] = content

        return self.render_to_response(context)
