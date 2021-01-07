from django import template
from projects.models import Project

register = template.Library()


#
# @register.inclusion_tag('projects/add_modal.html', takes_context=True)
# def show_results(context):
#     # non_ref_projects = Project.objects.filter(is_the_reference_project=False,
#     #                                           organization=context['organization'])
#     return {'form': context['form'],
#             'item_type': 'project',
#             'checkboxfields': 'wip'}


@register.inclusion_tag('projects/project_table_row.html')
def render_row(project):
    return {'project': project}
