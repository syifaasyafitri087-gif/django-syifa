from django.db import models
from django.contrib.auth.models import User

# 💎 MODEL DATA NAMA
class Nama(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='nama_list'
    )
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} ({self.user.username})"