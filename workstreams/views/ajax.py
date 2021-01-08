from django.shortcuts import render
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.template.loader import render_to_string

from workstreams.models import Workstream


def update_workstreams_table(request, project_id):
    data = dict()
    if request.method == 'GET':
        workstreams = Workstream.objects.filter(project_id=project_id)
        data['table'] = render_to_string(
            'workstreams/_workstreams_table.html',
            {'workstreams': workstreams},
            request=request
        )
        return JsonResponse(data)
