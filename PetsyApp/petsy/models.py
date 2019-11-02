from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(max_length=500, blank=True, default="default_user.png")
    description = models.TextField(blank=True)
    init_date = models.DateField(null=True, blank=True)
    following_users = ['paco', 'pepe']
    follower_count = models.IntegerField(default=0)
    favorite_products = models.IntegerField(default=0)