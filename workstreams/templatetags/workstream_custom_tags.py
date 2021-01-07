from django import template
from projects.models import Project

register = template.Library()


@register.inclusion_tag('workstreams/workstreams_table_row.html')
def render_row(workstream):
    return {'workstream': workstream}
