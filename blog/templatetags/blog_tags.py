from django import template

register = template.Library()


@register.filter
def is_following(from_user, to_user):
    return from_user.is_follow(to_user)
