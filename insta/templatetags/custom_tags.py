from django import template

register = template.Library()

@register.simple_tag
def is_following(current_user, background_user):
    return background_user.get_followers().filter(creator=current_user).exists()
