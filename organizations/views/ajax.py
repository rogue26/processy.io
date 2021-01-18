from django.http import HttpResponse
from django.http import JsonResponse

from projects.models import WorkstreamType, DeliverableType, TaskType, ConditionType, SpecificationType
from ..models import Content


def ajax_add_organization(request):
    data = dict()
    if request.method == 'GET':
        data['data'] = ""
        return JsonResponse(data)


def content_download(request):
    if request.method == 'GET':
        content = Content.objects.get(id=request.GET['content_id'])
        return HttpResponse(content.file.url)
    else:
        return HttpResponse("unsuccesful")


def add_workstream_type(request):
    if request.method == 'POST':
        newval = request.POST.get('newval')
        item = WorkstreamType.objects.create(name=newval)
        item.organization = request.user.organization
        item.save()
        return HttpResponse(item.id)


def add_deliverable_type(request):
    if request.method == 'POST':
        newval = request.POST.get('newval')
        item = DeliverableType.objects.create(name=newval)
        item.organization = request.user.organization
        item.save()
        return HttpResponse(item.id)


def add_task_type(request):
    if request.method == 'POST':
        newval = request.POST.get('newval')
        item = TaskType.objects.create(name=newval)
        item.organization = request.user.organization
        item.save()
        return HttpResponse(item.id)


def add_specification_type(request):
    if request.method == 'POST':
        newval = request.POST.get('newval')
        item = SpecificationType.objects.create(name=newval)
        item.organization = request.user.organization
        item.save()
        return HttpResponse(item.id)


def add_condition_type(request):
    if request.method == 'POST':
        newval = request.POST.get('newval')
        item = ConditionType.objects.create(name=newval)
        item.organization = request.user.organization
        item.save()
        return HttpResponse(item.id)


def edit_workstream_type(request):
    if request.method == 'POST':
        item = WorkstreamType.objects.get(id=request.POST.get('modelid'))
        item.name = request.POST.get('newval')
        item.save()
        return HttpResponse('success')


def edit_deliverable_type(request):
    if request.method == 'POST':
        item = DeliverableType.objects.get(id=request.POST.get('modelid'))
        item.name = request.POST.get('newval')
        item.save()
        return HttpResponse('success')


def edit_task_type(request):
    if request.method == 'POST':
        item = TaskType.objects.get(id=request.POST.get('modelid'))
        item.name = request.POST.get('newval')
        item.save()
        return HttpResponse('success')


def edit_condition_type(request):
    if request.method == 'POST':
        item = ConditionType.objects.get(id=request.POST.get('modelid'))
        item.name = request.POST.get('newval')
        item.save()
        return HttpResponse('success')


def edit_specification_type(request):
    if request.method == 'POST':
        item = SpecificationType.objects.get(id=request.POST.get('modelid'))
        item.name = request.POST.get('newval')
        item.save()
        return HttpResponse('success')


def delete_workstream_type(request):
    if request.method == 'POST':
        WorkstreamType.objects.get(id=request.POST.get('modelid')).delete()
        return HttpResponse('success')


def delete_deliverable_type(request):
    if request.method == 'POST':
        DeliverableType.objects.get(id=request.POST.get('modelid')).delete()
        return HttpResponse('success')


def delete_task_type(request):
    if request.method == 'POST':
        TaskType.objects.get(id=request.POST.get('modelid')).delete()
        return HttpResponse('success')


def delete_condition_type(request):
    if request.method == 'POST':
        ConditionType.objects.get(id=request.POST.get('modelid')).delete()
        return HttpResponse('success')


def delete_specification_type(request):
    if request.method == 'POST':
        SpecificationType.objects.get(id=request.POST.get('modelid')).delete()
        return HttpResponse('success')


def update_declined_organization(request):
    if request.method == 'POST':
        user = request.user
        user.declined_organization = True
        user.save()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)
