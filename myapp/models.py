from django.db import models

from django.contrib.auth.models import User

# =========================

# PROFILE USER

# =========================

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    foto = models.ImageField(upload_to='profile/', default='default.png')

    bio = models.TextField(blank=True, null=True)

    def __str__(self):

        return self.user.username

# =========================

# POSTINGAN

# =========================

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    caption = models.TextField()

    image = models.ImageField(upload_to='post/')

    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):

        return self.like_set.count()

    def __str__(self):

        return self.user.username

# =========================

# LIKE

# =========================

class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.user.username} suka postingan"

# =========================

# KOMENTAR

# =========================

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    isi = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username

# =========================

# FOLLOW TEMAN

# =========================

class Follow(models.Model):

    follower = models.ForeignKey(

        User,

        related_name='following',

        on_delete=models.CASCADE

    )

    following = models.ForeignKey(

        User,

        related_name='followers',

        on_delete=models.CASCADE

    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('follower', 'following')

    def __str__(self):

        return f"{self.follower.username} follow {self.following.username}"