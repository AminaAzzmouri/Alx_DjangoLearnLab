# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    # keep as URLField to avoid forcing Pillow/media setup in this first task
    profile_picture = models.URLField(blank=True)

    # non-symmetrical followers: A follows B doesn't imply B follows A
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )

    def __str__(self):
        return self.username
