from django import template
from blog.models import author_is_follow

register = template.Library()


@register.filter
def is_following(from_user, to_user):
    return author_is_follow(from_user, to_user)
