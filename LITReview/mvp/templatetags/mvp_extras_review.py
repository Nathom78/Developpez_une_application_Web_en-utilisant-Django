from django import template

from ..models import Review

register = template.Library()


@register.filter
def review_exist(ticket):
    if Review.objects.filter(ticket=ticket).exists():
        return True
    else:
        return False
    