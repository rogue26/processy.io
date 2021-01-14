from bootstrap_modal_forms.generic import BSModalFormView
from projects.models import Project, Workstream, Deliverable, Task, TeamMember
from projects.forms import ProjectForm, WorkstreamForm, DeliverableForm, TaskForm, TeamMemberForm

"""
Developer's note: You are probably wondering why on earth I have implemented object deletion in this 
hacky way rather than using BSModalDeleteView. The answer is that as of 20210110, asyncronous deletion
has not yet been implemented in django bootstrap modal forms. There /is/ an open pull request, however.
See issue https://github.com/trco/django-bootstrap-modal-forms/issues/123 and pull request 
https://github.com/trco/django-bootstrap-modal-forms/pull/126. If/when this gets implemented, these
views should definitely be rewritten using BSModalDeleteView.
"""


class DeleteProject(BSModalFormView):
    template_name = 'modals/delete.html'
    form_class = ProjectForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('asyncUpdate') == 'True':
            Project.objects.filter(id=self.kwargs['item_id']).delete()
        return super().post(request, *args, **kwargs)


class DeleteWorkstream(BSModalFormView):
    template_name = 'modals/delete.html'
    form_class = WorkstreamForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('asyncUpdate') == 'True':
            Workstream.objects.filter(id=self.kwargs['item_id']).delete()
        return super().post(request, *args, **kwargs)


class DeleteDeliverable(BSModalFormView):
    template_name = 'modals/delete.html'
    form_class = DeliverableForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('asyncUpdate') == 'True':
            Deliverable.objects.filter(id=self.kwargs['item_id']).delete()
        return super().post(request, *args, **kwargs)


class DeleteTask(BSModalFormView):
    template_name = 'modals/delete.html'
    form_class = TaskForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('asyncUpdate') == 'True':
            Task.objects.filter(id=self.kwargs['item_id']).delete()
        return super().post(request, *args, **kwargs)


class DeleteTeamMember(BSModalFormView):
    template_name = 'modals/delete.html'
    form_class = TeamMemberForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.POST.get('asyncUpdate') == 'True':
            TeamMember.objects.filter(id=self.kwargs['item_id']).delete()
        return super().post(request, *args, **kwargs)
