from django import template

register = template.Library()


@register.filter
def is_following(from_user, to_user):
    if from_user.is_authenticated() and to_user.is_authenticated():
        return from_user.following_set.filter(to_user=to_user).exists()
    return False
