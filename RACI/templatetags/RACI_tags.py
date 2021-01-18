from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag('RACI/tables/activity_table_row.html')
def render_activity_row(activity):
    context = dict()
    context['activity'] = activity
    return context

@register.inclusion_tag('RACI/tables/RACI_table_row.html')
def render_RACI_row(activity):
    context = dict()
    context['activity'] = activity
    return context
