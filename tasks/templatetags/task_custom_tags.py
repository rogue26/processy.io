from django import template
from projects.models import Project

register = template.Library()


@register.inclusion_tag('tasks/tasks_table_row.html')
def render_row(task):
    return {'task': task}
