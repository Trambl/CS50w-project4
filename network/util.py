from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Post, Comment, Like, Follow


def show_posts(user=None):
    if user:
        posts = Post.objects.filter(user=user)
    else:
        posts = Post.objects.all().order_by('-timestamp')
    post_data = []
    for post in posts:
        num_likes = post.likes.count()
        num_comments = post.comments.count()
        post_data.append({
            "post": post,
            "num_likes": num_likes,
            "num_comments": num_comments,
        })
    return post_data