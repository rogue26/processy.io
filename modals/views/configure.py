from django.conf import settings
from django.http import HttpResponseRedirect

from bootstrap_modal_forms.generic import BSModalFormView
from projects.models import Project, Workstream, WorkstreamType, Deliverable, DeliverableType, Task, TaskType, \
    TeamMember, Specification, Condition, Resource
from projects.forms import WorkstreamForm, DeliverableForm, TaskForm, TeamMemberForm




class ConfigureWorkstream(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = WorkstreamForm
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # I /guess/ this is the best place to initialize an instance variable?
        self.workstream = Workstream.objects.get(id=self.kwargs['item_id'])
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ConfigureWorkstream, self).get_form()
        form.fields['deliverables'].queryset = Deliverable.objects.filter(project=self.workstream.project)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['project'] = self.workstream.project
        context['header_text'] = "Add new workstream"
        context['button_text'] = "Save workstream"

        selected_deliverables = Deliverable.objects.filter(workstream=self.workstream)
        context["selected_deliverables"] = [_.id for _ in selected_deliverables]
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        initial = super().get_initial()
        initial['name'] = self.workstream.name
        initial['category'] = self.workstream.category
        initial['description'] = self.workstream.description
        initial['objective'] = self.workstream.objective
        initial['motivation'] = self.workstream.motivation
        initial['owner'] = self.workstream.owner

        return initial

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            updated_form_data = self.request.POST

            self.workstream.category = WorkstreamType.objects.get(id=updated_form_data.get('category'))
            self.workstream.name = updated_form_data.get('name')
            self.workstream.description = updated_form_data.get('description')
            self.workstream.objective = updated_form_data.get('objective')
            self.workstream.motivation = updated_form_data.get('motivation')
            self.workstream.owner = updated_form_data.get('owner')

            deliverables = Deliverable.objects.filter(pk__in=updated_form_data.getlist('deliverables'))
            self.workstream.deliverable_set.set(deliverables)

            self.workstream.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())


class ConfigureDeliverable(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = DeliverableForm
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # I /guess/ this is the best place to initialize an instance variable?
        self.deliverable = Deliverable.objects.get(id=self.kwargs['item_id'])
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ConfigureDeliverable, self).get_form()
        # form.fields['workstreams'].queryset = Workstream.objects.filter(project_id=self.kwargs['project_id'])
        form.fields['tasks'].queryset = Task.objects.filter(project=self.deliverable.project)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.deliverable.project
        context['header_text'] = "Add new deliverable"
        context['button_text'] = "Save deliverable"

        # todo: write these as one query and get id values
        selected_tasks = Task.objects.filter(deliverable=self.deliverable)
        context["selected_tasks"] = [_.id for _ in selected_tasks]
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial['name'] = self.deliverable.name
        initial['category'] = self.deliverable.category
        initial['description'] = self.deliverable.description
        initial['scope'] = self.deliverable.scope
        initial['workstream'] = self.deliverable.workstream

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template
        return initial

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            updated_form_data = self.request.POST

            self.deliverable.name = updated_form_data.get('name')
            self.deliverable.category = DeliverableType.objects.get(id=updated_form_data.get('category'))
            self.deliverable.description = updated_form_data.get('description')
            self.deliverable.scope = updated_form_data.get('scope')
            self.deliverable.workstream = Workstream.objects.get(id=updated_form_data.get('workstream'))

            specifications = Specification.objects.filter(pk__in=updated_form_data.getlist('specifications'))
            self.deliverable.specification_set.set(specifications)

            conditions = Condition.objects.filter(pk__in=updated_form_data.getlist('conditions'))
            self.deliverable.condition_set.set(conditions)

            tasks = Task.objects.filter(pk__in=updated_form_data.getlist('tasks'))
            self.deliverable.task_set.set(tasks)

            self.deliverable.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())


class ConfigureTask(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = TaskForm
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # I /guess/ this is the best place to initialize an instance variable?
        self.task = Task.objects.get(id=kwargs['item_id'])
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form()
        # form.fields['deliverables'].queryset = Deliverable.objects.filter(project=self.task.project)
        form.fields['parent_tasks'].queryset = Task.objects.filter(project=self.task.project).exclude(
            id=self.task.id)
        # form.fields['team_members'].queryset = TeamMember.objects.filter(project=self.task.project)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.task.project
        context['header_text'] = "Add new task"
        context['button_text'] = "Save task"

        context["selected_parent_tasks"] = self.task.parent_tasks.values_list('id', flat=True)
        # context["selected_required_resources"] = self.task.required_resources.values_list('id', flat=True)
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial['name'] = self.task.name
        initial['description'] = self.task.description
        initial['category'] = self.task.category

        initial['baseline_fte_days'] = self.task.baseline_fte_days
        initial['start'] = self.task.start
        initial['end'] = self.task.end
        initial['deliverable'] = self.task.deliverable
        # initial['status'] = current_task.status
        initial['team_member'] = self.task.team_member

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template
        return initial

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
            updated_form_data = self.request.POST

            self.task.name = updated_form_data.get('name')
            self.task.description = updated_form_data.get('description')
            self.task.category = TaskType.objects.get(id=updated_form_data.get('category'))
            self.task.baseline_fte_days = updated_form_data.get('baseline_fte_days')
            self.task.status = updated_form_data.get('status')

            try:
                self.task.team_member = updated_form_data.get('team_member')
            except ValueError:
                self.task.team_member = None

            self.task.deliverable = Deliverable.objects.get(id=updated_form_data.get('deliverable'))
            self.task.resources_required.set(
                Resource.objects.filter(pk__in=updated_form_data.getlist('resources_required')))

            self.task.parent_tasks.set(Task.objects.filter(pk__in=updated_form_data.getlist('parent_tasks')))

            # self.task.complexity_drivers.set(
            #     ComplexityDriver.objects.filter(pk__in=updated_form_data.getlist('complexity_drivers')))

            self.task.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())


class ConfigureTeamMember(BSModalFormView):
    template_name = 'modals/add_edit.html'
    form_class = TeamMemberForm
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # I /guess/ this is the best place to initialize an instance variable?
        self.team_member = TeamMember.objects.get(id=kwargs['item_id'])
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['user'].queryset = settings.AUTH_USER_MODEL.objects.filter(
            organization=self.request.user.organization)
        form.fields['tasks'].queryset = Task.objects.filter(project=self.team_member.project)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = "Add new"
        context['button_text'] = "Add"

        context["selected_tasks"] = Task.objects \
            .filter(team_member=self.team_member) \
            .values_list('id', flat=True)
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial['user'] = self.team_member.user
        initial['first_name'] = self.team_member.first_name
        initial['last_name'] = self.team_member.last_name
        initial['project_availability'] = self.team_member.project_availability

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template
        return initial

    def form_valid(self, form):
        if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':

            self.team_member.first_name = self.request.POST.get('first_name')
            self.team_member.last_name = self.request.POST.get('last_name')
            self.team_member.project_availability = self.request.POST.get('project_availability')
            self.team_member.save()

            task_ids_assigned = self.request.POST.getlist('tasks')
            team_member_tasks = Task.objects.filter(team_member=self.team_member)
            team_member_tasks.update(team_member=None)

            tasks_assigned = Task.objects.filter(id__in=task_ids_assigned)
            tasks_assigned.update(team_member=self.team_member)
            tasks_to_be_saved = team_member_tasks | tasks_assigned
            for task in tasks_to_be_saved.distinct():
                task.save()
        else:
            pass
        return HttpResponseRedirect(self.get_success_url())
