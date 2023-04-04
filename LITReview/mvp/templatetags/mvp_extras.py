# mvp/templatetags/mvp_extras.py
from django import template


register = template.Library()


@register.filter
def model_type(value):
    """Replaced by annotate in context"""
    return type(value).__name__


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def get_range_one_to_x(value):
    list_of_one_to_value = []
    for i in range(1, value + 1):
        list_of_one_to_value += [i]
    return list_of_one_to_value


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'Tu'
    return user.username
