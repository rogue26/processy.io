from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView, BSModalDeleteView

from .forms import TeamMemberForm
from .models import TeamMember
from users.models import CustomUser
from tasks.models import Task


class AddTeamMember(BSModalFormView):
    template_name = 'teams/add-team-member.html'
    form_class = TeamMemberForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(AddTeamMember, self).get_form()
        form.fields['user'].queryset = CustomUser.objects.filter(organization=self.request.user.organization)
        form.fields['tasks'].queryset = Task.objects.filter(project_id=self.kwargs['project_id'])
        return form

    # def get(self, request, *args, **kwargs):
    #     """Handle GET requests: instantiate a blank version of the form."""
    #
    #     context = self.get_context_data()
    #     context['project_id'] = self.kwargs['project_id']
    #     return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
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
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})


class ConfigureTeamMember(BSModalFormView):
    template_name = 'teams/configure-team-member.html'
    form_class = TeamMemberForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ConfigureTeamMember, self).get_form()
        form.fields['user'].queryset = CustomUser.objects.filter(organization=self.request.user.organization)
        form.fields['tasks'].queryset = Task.objects.filter(project_id=self.kwargs['project_id'])
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["selected_tasks"] = \
            [_.id for _ in Task.objects.filter(team_member_id=self.kwargs['team_member_id'])]
        return context

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        current_team_member = TeamMember.objects.get(id=self.kwargs['team_member_id'])

        initial = super().get_initial()

        initial['user'] = current_team_member.user
        initial['first_name'] = current_team_member.first_name
        initial['last_name'] = current_team_member.last_name
        initial['project_availability'] = current_team_member.project_availability

        # note - manytomany and foreignkey fields are set by passing the list of currently checked
        # items and setting the appropriate check value in the template

        return initial

    # def get(self, request, *args, **kwargs):
    #     """Handle GET requests: instantiate a blank version of the form."""
    #
    #     context = self.get_context_data()
    #     context['project_id'] = self.kwargs['project_id']
    #     return self.render_to_response(context)

    def form_valid(self, form):
        if not self.request.is_ajax():
            # team_member = form.save()
            # team_member.project_id = self.kwargs['project_id']
            # team_member.save()

            team_member = TeamMember.objects.get(id=self.kwargs['team_member_id'])
            team_member.first_name = self.request.POST.get('first_name')
            team_member.last_name = self.request.POST.get('last_name')
            team_member.project_availability = self.request.POST.get('project_availability')

            team_member.save()

            task_ids_assigned = self.request.POST.getlist('tasks')

            team_member_tasks = Task.objects.filter(team_member=team_member)
            team_member_tasks.update(team_member=None)

            tasks_assigned = Task.objects.filter(id__in=task_ids_assigned)
            tasks_assigned.update(team_member=team_member)

            tasks_to_be_saved = team_member_tasks | tasks_assigned
            for task in tasks_to_be_saved.distinct():
                task.save()

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})


class DeleteTeamMember(BSModalDeleteView):
    model = TeamMember
    template_name = 'teams/delete-team-member.html'
    success_message = 'Success: Team member was removed.'

    def get_success_url(self):
        return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})
