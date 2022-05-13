from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Create your models here.
class Post (models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20, blank=True)
    content = models.TextField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=None)