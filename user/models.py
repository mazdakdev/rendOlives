
from django.db import models
from django.contrib.auth.models import AbstractUser
from .myusermanager import MyUserManager



class MyUser(AbstractUser):
    username = None
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    backend = 'user.mybackend.ModelBackend'


class OrderAddress(models.Model):
    user = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=11)
    company = models.CharField(max_length=100 , blank=True , null=True)
    city = models.CharField(max_length=100)
    ostan = models.CharField(max_length=100)
    postal_code = models.IntegerField(blank=True , null=True)
    address = models.TextField()
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
