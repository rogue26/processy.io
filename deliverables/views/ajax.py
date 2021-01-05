from django.http import HttpResponse
from deliverables.models import SpecificationType, ConditionType


def update_spectype_condtype(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        model_id = request.POST.get('modelid')
        newval = request.POST.get('newval')

        if model_type == 'specificationtype':
            specification_type = SpecificationType.objects.get(id=model_id)
            specification_type.name = newval
            specification_type.save()
        elif model_type == 'conditiontype':
            condition_type = ConditionType.objects.get(id=model_id)
            condition_type.name = newval
            condition_type.save()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)


def add_spectype_condtype(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        deliverabletype_id = request.POST.get('deliverabletype_id')
        newval = request.POST.get('newval')

        if model_type == 'specificationtype':
            specification_type = SpecificationType(name=newval)
            specification_type.save()
            specification_type.deliverable_type_id = deliverabletype_id
            specification_type.save()
            new_id = specification_type.id
            return HttpResponse(new_id)

        elif model_type == 'conditiontype':
            condition_type = ConditionType(name=newval)
            condition_type.save()
            condition_type.deliverable_type_id = deliverabletype_id
            condition_type.save()
            new_id = condition_type.id
            return HttpResponse(new_id)

    else:
        message = 'update unsuccessful'
        return HttpResponse(message)


def delete_spectype_condtype(request):
    if request.method == 'POST':

        model_type = request.POST.get('modeltype')
        model_id = request.POST.get('modelid')

        print('model_id = ', model_id)

        if model_type == 'specificationtype':
            SpecificationType.objects.get(id=model_id).delete()

        elif model_type == 'conditiontype':
            ConditionType.objects.get(id=model_id).delete()

        message = 'update successful'
    else:
        message = 'update unsuccessful'
    return HttpResponse(message)
