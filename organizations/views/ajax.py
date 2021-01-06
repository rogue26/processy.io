from django.http import HttpResponse

from deliverables.models import SpecificationType, ConditionType
from projects.models import Project
from workstreams.models import WorkstreamType
from tasks.models import TaskType

def update_type(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        model_id = request.POST.get('modelid')
        newval = request.POST.get('newval')

        if model_type == 'specificationtype':
            item = SpecificationType.objects.get(id=model_id)
            item.name = newval
            item.save()
        elif model_type == 'conditiontype':
            item = ConditionType.objects.get(id=model_id)
            item.name = newval
            item.save()
        elif model_type == 'workstreamtype':
            item = WorkstreamType.objects.get(id=model_id)
            item.name = newval
            item.save()
        elif model_type == 'tasktype':
            item = TaskType.objects.get(id=model_id)
            item.name = newval
            item.save()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)


def add_type(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        deliverabletype_id = request.POST.get('deliverabletype_id')
        newval = request.POST.get('newval')

        if model_type == 'specificationtype':
            item = SpecificationType(name=newval)
            item.save()
            item.deliverable_type_id = deliverabletype_id
            item.save()
            new_id = item.id
            return HttpResponse(new_id)

        elif model_type == 'conditiontype':
            item = ConditionType(name=newval)
            item.save()
            item.deliverable_type_id = deliverabletype_id
            item.save()
            new_id = item.id
            return HttpResponse(new_id)

        elif model_type == 'workstreamtype':
            item = WorkstreamType(name=newval)
            item.save()
            item.organization = request.user.organization
            item.save()
            new_id = item.id
            return HttpResponse(new_id)

        elif model_type == 'tasktype':
            item = TaskType(name=newval)
            item.save()
            item.organization = request.user.organization
            item.save()
            new_id = item.id
            return HttpResponse(new_id)

    else:
        message = 'update unsuccessful'
        return HttpResponse(message)


def delete_type(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        model_id = request.POST.get('modelid')

        if model_type == 'specificationtype':
            SpecificationType.objects.get(id=model_id).delete()

        elif model_type == 'conditiontype':
            ConditionType.objects.get(id=model_id).delete()

        elif model_type == 'workstreamtype':
            WorkstreamType.objects.get(id=model_id).delete()

        elif model_type == 'tasktype':
            TaskType.objects.get(id=model_id).delete()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)


def update_declined_organization(request):
    if request.method == 'POST':
        user = request.user
        user.declined_organization = True
        user.save()

        ref_project = Project()
        ref_project.name = "Reference project"
        ref_project.description = "Placeholder project for holding an organization's default workstreams."
        ref_project.client = user.email
        ref_project.is_the_reference_project = True

        ref_project.save()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)
