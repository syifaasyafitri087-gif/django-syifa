from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# =========================
# POSTINGAN
# =========================
class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to='post/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True
    )

    caption = models.TextField(
        blank=True,
        null=True
    )

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.user.username


# =========================
# KOMENTAR
# =========================
class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


# =========================
# PROFILE PREMIUM
# =========================
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to='profile/',
        default='default.png'
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    verified = models.BooleanField(
        default=False
    )

    is_online = models.BooleanField(
        default=False
    )

    last_seen = models.DateTimeField(
        default=timezone.now
    )

    typing_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='typing_users'
    )

    def __str__(self):
        return self.user.username


# =========================
# FOLLOW
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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


# =========================
# STORY
# =========================
class Story(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='stories/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_active(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return self.user.username


# =========================
# FULL CHAT MESSAGE
# =========================
class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    text = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='chat/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    delivered = models.BooleanField(
        default=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"