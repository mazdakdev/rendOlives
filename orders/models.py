from django.db import models
from shop.models import Product, ProductSizes, product
from django.contrib.auth.models import User

from user.models import MyUser
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save
from user.models import MyUser


# Create your models here.

ORDER_STATUS_CHOICES= (
    ('در حال انجام', 'در حال انحام'),
    ('تکمیل شده', 'تکمیل شده'),
    ('لغو شده', 'لغو شده'),
    ('معلق', 'معلق'),
    )

ORDER_METHOD_CHOICES= (
    ('ارسال معمولی', 'ارسال معمولی'),
    ('ارسال رایگان', 'ارسال رایگان'),
    ('تیپاکس', 'تیپاکس'),
    )

class Order(models.Model):
    order_id= models.CharField(max_length=120, blank= True)
    user = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=11)
    email = models.EmailField(blank=True , null=True)
    company = models.CharField(max_length=100 , blank=True , null=True)
    city = models.CharField(max_length=100)
    ostan = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20 , blank=True , null=True)
    address = models.TextField()
    extra_desc = models.TextField(blank=True , null=True)
    country = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    status= models.CharField(max_length=120, default='در حال انجام', choices= ORDER_STATUS_CHOICES)
    method = models.CharField(max_length=120 , choices=ORDER_METHOD_CHOICES , default="ارسال معمولی" )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

def pre_save_create_order_id(sender, instance, *args, **kwargs):
        if not instance.order_id:
            instance.order_id= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

class OrderItems(models.Model):
    order = models.ForeignKey(Order ,  related_name="items" , on_delete=models.CASCADE)
    product = models.ForeignKey(ProductSizes , related_name="order_items" , on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=True , null=True )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
