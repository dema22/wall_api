from django.db import models

# Create your models here.
class Post (models.Model):
    created_at = models.DateTimeField(null=True)
    title = models.CharField(max_length=20, blank=True)
    content = models.TextField()