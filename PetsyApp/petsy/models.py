from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

from productManagerApp.models import Product, Shop


class UserPetsy(User):
    photo = models.ImageField(max_length=500, blank=True, default="default_user.png")
    description = models.TextField(blank=True)
    init_date = models.DateField(null=True, blank=True)
    following_users = models.ManyToManyField(User)
    follower_count = models.ManyToManyField(User)
    favorite_products = models.ManyToManyField(Product)
    shop_list = models.ForeignKey(Shop, on_delete=models.CASCADE())
