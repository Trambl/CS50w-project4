from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Post, Comment, Like, Follow


def show_posts(user=None, page_number=None):
    if user is not None:
        if hasattr(user, '__iter__'):
            posts = Post.objects.filter(user__in=user).order_by('-timestamp')
        else:
            posts = Post.objects.filter(user=user).order_by('-timestamp')
    else:
        posts = Post.objects.all().order_by('-timestamp')
        
    post_data = [{
        "post": post,
        "num_likes": post.likes.count(),
        "num_comments": post.comments.count(),
    } for post in posts]
    paginator = Paginator(post_data, 10)
    page_obj = paginator.get_page(page_number)
    return page_obj, paginator
