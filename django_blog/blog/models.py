from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone  # Needed for default

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)  # Add this field
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
