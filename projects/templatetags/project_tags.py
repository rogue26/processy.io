from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.simple_tag
def form_group_id_modal(field):
    return str(field.auto_id) + "_group_modal"


@register.simple_tag
def form_group_id(field):
    return str(field.auto_id) + "_group"


@register.simple_tag
def form_group_style(field):
    try:
        if "initial-hide" in field.field.widget.attrs['class']:
            return "style=display:none;"
    except KeyError:
        return


@register.inclusion_tag('projects/tables/projects_table_row.html')
def render_project_row(project):
    return {'project': project}


@register.inclusion_tag('projects/tables/workstreams_table_row.html')
def render_workstream_row(workstream):
    context = dict()
    context['workstream'] = workstream
    context['edit_form_url'] = reverse_lazy('modals:configure_workstream',
                                            kwargs={'item_id': workstream.id})
    context['delete_form_url'] = reverse_lazy('modals:delete_workstream',
                                              kwargs={'item_id': workstream.id})
    context['data_url'] = reverse_lazy('projects:update_workstreams_table',
                                       kwargs={'project_id': workstream.project.id})
    context['modal_id'] = "#create-modal"
    context['data_element_id'] = "#workstreams-table"
    return context


@register.inclusion_tag('projects/tables/deliverables_table_row.html')
def render_deliverable_row(deliverable):
    context = dict()
    context['deliverable'] = deliverable
    context['edit_form_url'] = reverse_lazy('modals:configure_deliverable',
                                            kwargs={'item_id': deliverable.id})
    context['delete_form_url'] = reverse_lazy('modals:delete_deliverable',
                                              kwargs={'item_id': deliverable.id})
    context['data_url'] = reverse_lazy('projects:update_deliverables_table',
                                       kwargs={'project_id': deliverable.project.id})
    context['modal_id'] = "#create-modal"
    context['data_element_id'] = "#deliverables-table"
    return context


@register.inclusion_tag('projects/tables/tasks_table_row.html')
def render_task_row(task):
    context = dict()
    context['task'] = task
    context['edit_form_url'] = reverse_lazy('modals:configure_task',
                                            kwargs={'item_id': task.id})
    context['delete_form_url'] = reverse_lazy('modals:delete_task',
                                              kwargs={'item_id': task.id})
    context['data_url'] = reverse_lazy('projects:update_tasks_table',
                                       kwargs={'project_id': task.project.id})
    context['modal_id'] = "#create-modal"
    context['data_element_id'] = "#tasks-table"
    return context


@register.inclusion_tag('projects/tables/team_members_table_row.html')
def render_teammember_row(team_member):
    return {'team_member': team_member}
