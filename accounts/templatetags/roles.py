from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='is_group')
def is_group(user : User, group : str) -> bool:
    return user.groups.filter(name=group).exists()