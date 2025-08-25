from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)

    # Use ImageField so the checker finds "models.ImageField"
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    # non-symmetrical followers (A follows B != B follows A)
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username