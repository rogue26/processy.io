from django import template
from projects.models import Project

register = template.Library()


@register.inclusion_tag('deliverables/deliverables_table_row.html')
def render_row(deliverable):
    return {'deliverable': deliverable}
