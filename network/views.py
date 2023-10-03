from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Post, Comment, Like, Follow
from .util import show_posts


def index(request):
    page_obj, paginator = show_posts(
        request=request, page_number=request.GET.get("page")
    )
    return render(
        request,
        "network/index.html",
        {
            "page_obj": page_obj,
            "paginator": paginator,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "network/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "network/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def submit_post(request):
    # TODO I'm trying to make an animation of new appearing post
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Extract the 'body' field from the data
        body = data.get("body", "")

        # Create a new Post instance and save it to the database
        post = Post(user=request.user, content=body)
        post.save()

        # Process the body data as needed
        return JsonResponse({"post": post.serialize()})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def profile(request, username):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        user_profile = User.objects.get(username=username)
        is_following = Follow.objects.filter(
            follower=request.user, following=user_profile
        ).exists()

        page_obj, paginator = show_posts(
            request=request,
            user=user_profile,
            page_number=request.GET.get("page"),
        )
        return render(
            request,
            "network/profile.html",
            {
                "user_profile": user_profile,
                "num_followers": user_profile.follower.count(),
                "num_followings": user_profile.following.count(),
                "is_following": is_following,
                "page_obj": page_obj,
                "paginator": paginator,
            },
        )
    if request.method == "POST":

        follower = request.user
        following = User.objects.get(username=username)
        followed = Follow.objects.filter(
            follower=follower, following=following
        ).exists()
        if followed:
            follow = Follow.objects.get(follower=follower, following=following)
            follow.delete()
            return JsonResponse(
                {
                    "followed": False,
                    "num_followers": following.follower.count(),
                    "num_followings": following.following.count(),
                }
            )
        else:
            follow = Follow(follower=follower, following=following)
            follow.save()
            return JsonResponse(
                {
                    "followed": True,
                    "num_followers": following.follower.count(),
                    "num_followings": following.following.count(),
                }
            )


def following_users(request, username):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        user = User.objects.get(username=username)
        following_users = Follow.objects.filter(follower=user).values(
            "following"
        )
        page_obj, paginator = show_posts(
            request=request,
            user=following_users,
            page_number=request.GET.get("page"),
        )
        return render(
            request,
            "network/following.html",
            {
                "page_obj": page_obj,
                "paginator": paginator,
            },
        )


def edit_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data["postId"]
        edited_content = data["editedContent"]

        # Update the post's content in the database
        post = Post.objects.get(pk=post_id)
        post.content = edited_content
        post.save()
        return JsonResponse(
            {
                "message": "Post updated successfully",
                "post_content": post.content,
            }
        )


def like_post(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        data = json.loads(request.body)
        post_id = data["postId"]
        user = request.user
        post = Post.objects.get(pk=post_id)
        liked = Like.objects.filter(user=user, post=post).exists()
        if liked:
            like = Like.objects.get(user=user, post=post)
            post.likes.remove(like)
            like.delete()

            return JsonResponse(
                {
                    "liked": False,
                    "num_likes": post.likes.count(),
                }
            )
        else:
            like = Like(user=user, post=post)
            like.save()
            post.likes.add(like)

            return JsonResponse(
                {
                    "liked": True,
                    "num_likes": post.likes.count(),
                }
            )
