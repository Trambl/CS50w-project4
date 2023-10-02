from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        "Like", related_name="liked_posts", blank=True
    )
    comments = models.ManyToManyField(
        "Comment", related_name="commented_posts", blank=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": self.likes.count(),
            "comments": self.comments.count(),
        }

    def __str__(self):
        return f"Post by {self.user.username} at {self.timestamp}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __str__(self):
        return f"Comment by {self.user.username} on post by {self.post.user.username}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.post:
            return f"Like by {self.user.username} on post by {self.post.user.username}"
        elif self.comment:
            return f"Like by {self.user.username} on comment by {self.comment.user.username}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    created_at = models.DateTimeField(auto_now_add=True)
