from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalFormView

from .forms import AddTeamMemberForm
from .models import TeamMember
from users.models import CustomUser
from tasks.models import Task

class AddTeamMember(BSModalFormView):
    template_name = 'teams/add-team-member.html'
    form_class = AddTeamMemberForm

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

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})


class ConfigureTeamMember(BSModalFormView):
    template_name = 'teams/configure-team-member.html'
    form_class = AddTeamMemberForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(ConfigureTeamMember, self).get_form()
        form.fields['user'].queryset = CustomUser.objects.filter(organization=self.request.user.organization)
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

        else:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('project', kwargs={'project_id': self.kwargs['project_id']})