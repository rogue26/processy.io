from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from projects.models import Project

register = template.Library()


# @register.filter(name='lower')
# @stringfilter  # use this if your filter only accepts strings
# def lower(value):
#     return value.lower()
#
#
# @register.filter(needs_autoescape=True)
# def initial_letter_filter(text, autoescape=True):
#     first, other = text[0], text[1:]
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     result = '<strong>%s</strong>%s' % (esc(first), esc(other))
#     return mark_safe(result)
#
#
# @register.simple_tag
# def current_time(format_string):
#     return datetime.now().strftime(format_string)


# register.simple_tag(lambda x: x - 1, name='minusone')
#
#
# @register.simple_tag(name='minustwo')
# def some_function(value):
#     return value - 2
#
#
# @register.simple_tag
# def my_tag(a, b, *args, **kwargs):
#     warning = kwargs['warning']
#     profile = kwargs['profile']
#     return warning


@register.inclusion_tag('organizations/tables/org_projects_table.html', takes_context=True)
def show_nonref_projects(context):
    non_ref_projects = Project.objects.filter(is_the_reference_project=False,
                                              organization=context['organization'])
    return {'non_ref_projects': non_ref_projects}
