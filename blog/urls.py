
from unicodedata import name
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.all_posts , name="all.posts"),
    path('search/', views.search , name="blog.search"),
    path('<slug:slug>/posts/', views.get_posts_by_category , name="get.post.category"),
    path('posts/<slug:slug>/', views.post , name="get.post"),

]
