from django.http import JsonResponse
from django.template.loader import render_to_string

from projects.models import WorkstreamType, Deliverable, Task, TeamMember
from projects.forms import WorkstreamForm

def update_dropdown_options(request):
    data = dict()
    if request.method == 'GET':

        form = WorkstreamForm()

        workstreamtypes = WorkstreamType.objects.filter(organization=request.user.organization)
        data['data'] = render_to_string(
            'modals/modal_choice_field.html',
            {'field': form.fields[0]},
            request=request
        )
        return JsonResponse(data)
