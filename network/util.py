from django.core.paginator import Paginator
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import User, Post, Comment, Like, Follow


def show_posts(user=None, page_number=None):
    if user is not None:
        if hasattr(user, "__iter__"):
            posts = Post.objects.filter(user__in=user).order_by("-timestamp")
        else:
            posts = Post.objects.filter(user=user).order_by("-timestamp")
    else:
        posts = Post.objects.all().order_by("-timestamp")

    post_data = [
        {
            "post": post,
            "num_likes": post.likes.count(),
            "num_comments": post.comments.count(),
        }
        for post in posts
    ]
    paginator = Paginator(post_data, 10)
    page_obj = paginator.get_page(page_number)
    return page_obj, paginator


register = template.Library()


@register.filter(is_safe=True)
def linebreaksbr(value, autoescape=True):
    """
    Convert newlines into <br> in HTML.
    """
    value = escape(value)
    value = value.replace("\n", "<br>")
    return mark_safe(value)


register.filter(linebreaksbr)
