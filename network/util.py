from django.core.paginator import Paginator
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import User, Post, Comment, Like, Follow


def show_posts(request, user=None, page_number=None):
    if user is not None:
        # Check if the 'user' variable is iterable (a list or queryset of users)
        if hasattr(user, "__iter__"):
            # If 'user' is iterable, filter posts by users in the iterable and order by timestamp
            posts = Post.objects.filter(user__in=user).order_by("-timestamp")
        else:
            # If 'user' is not iterable, filter posts by the single user and order by timestamp
            posts = Post.objects.filter(user=user).order_by("-timestamp")
    else:
        # If 'user' is None (no specific user specified), fetch all posts and order by timestamp
        posts = Post.objects.all().order_by("-timestamp")

    post_data = [
        {
            "post": post,
            "num_likes": post.likes.count(),
            "num_comments": post.comments.count(),
        }
        for post in posts
    ]

    if request.user.is_authenticated:
        for post_dict in post_data:
            post_dict["liked"] = Like.objects.filter(
                user=request.user, post=post_dict["post"]
            ).exists()
    else:
        for post in post_data:
            post["liked"] = False

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
