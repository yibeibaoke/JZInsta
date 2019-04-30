import re
from django import template

register = template.Library()

@register.simple_tag
def is_following(current_user, background_user):
    return background_user.get_followers().filter(creator=current_user).exists()

@register.filter(name='parse_hashtags')
def parse_hashtags(field):
    hashtags_arr = re.findall(r"#(\w+)", field)
    for hashtag in hashtags_arr:
        html_tag = "<a href='/explore?hashtag=" + hashtag + "'>#" + hashtag + "</a>"
        field = field.replace("#" + hashtag, html_tag)
    return field

@register.simple_tag
def has_user_liked_post(post, user):
    try:
        like = Like.objects.get(post=post, user=user)
        return "fa-heart"
    except:
        return "fa-heart-o"
