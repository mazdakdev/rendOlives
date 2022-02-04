
from django.db import models
from shop.models import Category
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category ,on_delete=models.CASCADE , blank=True ,null=True )
    body = models.TextField()
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to="blog/%Y/%m/%d" )
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def get_absolute_url(self):
      return reverse('get.post', kwargs={'slug': self.slug})
      