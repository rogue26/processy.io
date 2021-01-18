import json

from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.conf import settings

from bootstrap_modal_forms.generic import BSModalFormView, BSModalCreateView

from projects.models import (
    Project,
    Workstream,
    WorkstreamType,
    Deliverable,
    DeliverableType,
    Task,
    TaskType,
    TeamMember,
    Resource
)
from projects.forms import (
    ProjectModalForm,
    AddWorkstreamTypeForm,
    WorkstreamTypeForm,
    WorkstreamForm,
    DeliverableTypeForm,
    AddDeliverableTypeForm,
    DeliverableForm,
    TaskTypeForm,
    TeamMemberForm,
    TaskForm
)
from organizations.forms import ContentForm, DivisionForm, OrganizationModalForm


class AddOrganization(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = OrganizationModalForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new organization"
        context['button_text'] = "Save"
        context['explanatory_text'] = \
            "Before we get started, let's fill in some information about your organization.This will help " \
            "others in your organization to be able to see default project configurations and knowledge " \
            "management materials."
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddProject(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = ProjectModalForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['client'].widget.attrs.update({'class': 'initial-hide'})
        form.fields['internal'].widget.attrs.update({'id': 'id_internal_modal'})

        if self.request.user.organization:
            if not self.request.user.organization.division_set.all().exists():
                del form.fields['division']
        else:
            del form.fields['division']

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new project"
        context['button_text'] = "Save project"
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class AddWorkstream(BSModalFormView):
#     template_name = 'modals/add_edit.html'
#     form_class = WorkstreamTypeForm
#     success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url
#
#     # def get_form(self, form_class=None):
#     #     form = super(AddWorkstream, self).get_form()
#     #     form.fields['deliverables'].queryset = Deliverable.objects.filter(project_id=self.kwargs['project_id'])
#     # return form
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['project'] = Project.objects.get(id=self.kwargs['project_id'])
#         context['header_text'] = "Add new workstream"
#         context['button_text'] = "Save workstream"
#         return context
#
#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs.update({'project_id': self.kwargs['project_id']})
#     #     return kwargs
#
#     def form_valid(self, form):
#         # note, this must be done in the view rather than the form because workstreams, deliverables, and tasks are
#         # not created using a ModelForm. Types are selected (potentially multiple at once) and then the workstream,
#         # deliverable, and task objects are created in a loop
#         if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
#             types_to_add = self.request.POST.getlist('workstream_type')
#
#             project = Project.objects.get(id=self.kwargs['project_id'])
#             for type_num in types_to_add:
#                 workstream_type = WorkstreamType.objects.get(id=int(type_num))
#
#                 # if created for the reference project, then set is_the_default_workstream to True
#                 if project.is_the_reference_project:
#                     new_ws = Workstream.objects.create(name=workstream_type.name, description=workstream_type.name,
#                                                        category_id=int(type_num),
#                                                        project_id=self.kwargs['project_id'],
#                                                        is_the_reference_workstream=True)
#                     new_ws.save()
#                 else:
#                     # attempt to copy the reference workstream for this workstream category
#                     try:
#                         new_ws = Workstream.objects.filter(is_the_reference_workstream=True,
#                                                            category=workstream_type).first()
#                         reference_ws_id = new_ws.id
#                         old_deliverables = Deliverable.objects.filter(workstream_id=new_ws.id)
#
#                         new_ws.pk = None
#                         new_ws.project = project
#                         new_ws.is_the_reference_workstream = False
#                         new_ws.save()
#
#                         new_ws.copied_from_id = reference_ws_id
#                         new_ws.save()
#
#                         # now copy over all deliverables associated with the reference workstream
#                         for old_deliverable in old_deliverables:
#                             old_tasks = Task.objects.filter(deliverable_id=old_deliverable.id)
#                             reference_deliverable_id = old_deliverable.id
#                             old_deliverable.pk = None
#                             old_deliverable.project = project
#                             old_deliverable.is_the_reference_deliverable = False
#                             old_deliverable.workstream = new_ws
#                             old_deliverable.save()
#                             old_deliverable.copied_from_id = reference_deliverable_id
#                             old_deliverable.save()
#
#                             # copy over all tasks associated with this deliverable in the reference configuration
#                             for old_task in old_tasks:
#                                 reference_task_id = old_task.id
#                                 old_task.pk = None
#                                 old_task.project = project
#                                 old_task.is_the_reference_task = False
#                                 old_task.deliverable = old_deliverable
#                                 old_task.save()
#                                 old_task.copied_from_id = reference_task_id
#                                 old_task.save()
#                     except:
#                         new_ws = Workstream.objects.create(name=workstream_type.name, description=workstream_type.name,
#                                                            category_id=int(type_num),
#                                                            project_id=self.kwargs['project_id'],
#                                                            is_the_reference_workstream=False)
#                         new_ws.save()
#         else:
#             pass
#         return super().form_valid(form)


class AddWorkstream(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = WorkstreamForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['category'].queryset = WorkstreamType.objects.filter(organization=self.request.user.organization)

        form.fields['category'].widget.attrs.update({'class': 'modelchoicefield'})

        deliverables = Deliverable.objects.filter(project_id=self.kwargs['project_id'])
        if deliverables:
            form.fields['deliverables'].queryset = deliverables
            form.fields['deliverables'].widget.attrs.update({'class': 'modelchoicefield'})
        else:
            del form.fields['deliverables']
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        context['header_text'] = "Add new workstream"
        context['button_text'] = "Save workstream"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.instance.project_id = self.kwargs['project_id']
            form.save()
        else:
            pass
        return super().form_valid(form)


class AddDeliverable(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = DeliverableForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form()

        form.fields['category'].widget.attrs.update({'class': 'modelchoicefield'})

        workstreams = Workstream.objects.filter(project_id=self.kwargs['project_id'])
        if workstreams:
            form.fields['workstream'].queryset = workstreams
            form.fields['workstream'].widget.attrs.update({'class': 'modelchoicefield'})
        else:
            del form.fields['workstream']

        tasks = Task.objects.filter(project_id=self.kwargs['project_id'])
        if tasks:
            form.fields['tasks'].queryset = tasks
        else:
            del form.fields['tasks']

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        context['header_text'] = "Add new deliverable"
        context['button_text'] = "Save deliverable"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.instance.project_id = self.kwargs['project_id']
            form.save()
        else:
            pass
        return super().form_valid(form)


class AddTask(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = TaskForm
    success_url = '/'

    def get_form(self, form_class=None):
        form = super().get_form()

        form.fields['category'].widget.attrs.update({'class': 'modelchoicefield'})

        tasks = Task.objects.filter(project_id=self.kwargs['project_id'])
        if tasks:
            form.fields['parent_tasks'].queryset = Task.objects.filter(project_id=self.kwargs['project_id'])
            form.fields['deliverable'].widget.attrs.update({'class': 'modelmultichoicefield'})
        else:
            del form.fields['parent_tasks']

        team_members = TeamMember.objects.filter(project_id=self.kwargs['project_id'])
        if team_members:
            form.fields['team_member'].queryset = TeamMember.objects.filter(project_id=self.kwargs['project_id'])
            form.fields['team_member'].widget.attrs.update({'class': 'modelchoicefield'})
        else:
            del form.fields['team_member']
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        context['header_text'] = "Add new task"
        context['button_text'] = "Save task"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.instance.project_id = self.kwargs['project_id']
            form.save()
        else:
            pass
        return super().form_valid(form)


class AddContent(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = ContentForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_form(self, form_class=None):
        form = super(AddContent, self).get_form()
        form.fields['tasks'].queryset = Task.objects.filter(team_member__user=self.request.user,
                                                            project__is_the_reference_project=False)
        form.fields['deliverables'].queryset = Deliverable.objects.filter(Q(task__team_member__user=self.request.user))
        form.fields['workstreams'].queryset = Workstream.objects.filter(
            Q(deliverable__task__team_member__user=self.request.user))
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new knowledge management content"
        context['button_text'] = "Submit content"
        context['explanatory_text'] = \
            "Uploaded material will become available to help other teams working on similar workstreams, tasks, " \
            "and deliverables. If you select project components that were copied from an organizational default, " \
            "the uploaded material will automatically become available to any other projects that were copied from the " \
            "same default."
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'project_id': self.kwargs['project_id']})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddTeamMember(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = TeamMemberForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_form(self, form_class=None):
        form = super(AddTeamMember, self).get_form()
        form.fields['user'].queryset = settings.AUTH_USER_MODEL.objects.filter(
            organization=self.request.user.organization)
        form.fields['tasks'].queryset = Task.objects.filter(project_id=self.kwargs['project_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new team member"
        context['button_text'] = "Save"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            team_member = form.save()
            team_member.project_id = self.kwargs['project_id']
            team_member.save()
            task_ids_assigned = self.request.POST.getlist('tasks')
            tasks = Task.objects.filter(id__in=task_ids_assigned)
            tasks.update(team_member=team_member)
            for task in tasks:
                task.save()
        else:
            pass
        return super().form_valid(form)


class AddDivision(BSModalCreateView):
    template_name = 'organizations/add_division.html'
    form_class = DivisionForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.instance.organization = self.request.user.organization
            form.save()
        else:
            pass
        return super().form_valid(form)


class AddWorkstreamType(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = AddWorkstreamTypeForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new workstream type"
        context['button_text'] = "Save"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            form.instance.organization = self.request.user.organization
            form.save()
        else:
            pass
        return super().form_valid(form)


class AddDeliverableType(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = AddDeliverableTypeForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new deliverable type"
        context['button_text'] = "Save"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            deliverable_type = form.save()

            deliverable_type.organization = self.request.user.organization
            deliverable_type.save()
        else:
            pass
        return super().form_valid(form)


class AddTaskType(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = TaskTypeForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new task type"
        context['button_text'] = "Save"
        return context

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            task_type = form.save()

            task_type.organization = self.request.user.organization
            task_type.save()
        else:
            pass
        return super().form_valid(form)


class AddContentType(BSModalCreateView):
    template_name = 'modals/add_edit.html'
    form_class = TaskTypeForm
    success_url = "/"  # doesn't matter, because we're going to submit asyncronously and not use success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new content type"
        context['button_text'] = "Save"
        return context
