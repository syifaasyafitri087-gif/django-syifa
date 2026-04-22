from django.db import models
from django.contrib.auth.models import User


# =========================
# POSTINGAN
# =========================
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/')
    caption = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.user.username


# =========================
# KOMENTAR
# =========================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# =========================
# PROFILE USER
# =========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile/', default='default.png')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# =========================
# FOLLOW USER
# =========================
class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"