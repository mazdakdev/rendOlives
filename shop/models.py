from itertools import product
from operator import mod
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH, SlugField
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth.models import User

from user.models import MyUser

class Category(models.Model):
    name = models.CharField(max_length=200 , db_index=True )
    slug = models.SlugField(max_length=200 , db_index=True , unique=True )

    def get_absolute_url(self):
      return reverse('category.products', kwargs={'slug': self.slug})

    def get_absolute_url(self):
      return reverse('get.post.category', kwargs={'slug': self.slug})
      
    class Meta:
        ordering=("name",)

    def __str__(self):
        return self.name


    
class Brand(models.Model):
    name = models.CharField(max_length=200 , db_index=True)
    slug = models.SlugField(max_length=200 , db_index=True , unique=True)

    def get_absolute_url(self):
      return reverse('brand.products', kwargs={'slug': self.slug})
    class Meta:
        ordering=("name",)

    def __str__(self):
        return self.name

class ProductSizes(models.Model):
  name = models.CharField(max_length=50)
  price = models.IntegerField()
  off_price = models.IntegerField(blank=True , null=True)
  picture = models.ImageField(upload_to="products/%Y/%m/%d" )
  product = models.ForeignKey("Product" ,  on_delete=models.CASCADE )
  


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to="products/%Y/%m/%d" )
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category ,on_delete=models.CASCADE  )
    slug = models.SlugField(max_length=100 , db_index=True  , unique=True)
    tags = TaggableManager(blank=True)
    is_amazing = models.BooleanField(default=False)
    amazing_till = models.CharField(max_length=10 , null=True , blank=True)
    off_price = models.IntegerField(blank=True , null=True)
    brand = models.ForeignKey(Brand ,on_delete=models.CASCADE  )
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def get_absolute_url(self):
      return reverse('get.single.product', kwargs={'slug': self.slug})
      
    def get_absolute_url(self):
      return reverse('get.size', kwargs={'slug': self.slug})

    class Meta:
        ordering=("name",) 
        index_together = (('id' , 'slug'),)

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.user.first_name)

    def get_absolute_url(self):
      return reverse('add.comment', kwargs={'slug': Product.slug})

class WebInfo(models.Model):
    banner_1 = models.ImageField(upload_to="banners/%Y/%m/%d" )
    banner_2 = models.ImageField(upload_to="banners/%Y/%m/%d" , blank=True , null=True )
    banner_3 = models.ImageField(upload_to="banners/%Y/%m/%d" , blank=True , null=True)
    banner_4 = models.ImageField(upload_to="banners/%Y/%m/%d" , blank=True , null=True )
    small_banner_1 = models.ImageField(upload_to="banners/%Y/%m/%d" , blank=True , null=True )
    small_banner_2 = models.ImageField(upload_to="banners/%Y/%m/%d" , blank=True , null=True )
    footertext = models.TextField()    


