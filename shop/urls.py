from django.contrib import admin
from django.urls import path , include
from . import  views


urlpatterns = [
    path('', views.HomeView , name="home" ),
    path("<slug:slug>/products/" , views.get_product_by_category , name="category.products"),
    path("brand/<slug:slug>/products/" , views.get_product_by_brand , name="brand.products"),
    path("products/<slug:slug>" , views.get_product_by_slug , name="get.single.product"),
    path("products/<slug:slug>/comment/" , views.add_comment , name="add.comment"),
    path("products/" , views.shop , name="all.products"),
    path("cart/" , include("cart.urls") ),
    path("orders/" , include("orders.urls") ),
    path("about-us/" , views.about_us , name="about.us" ),
    path("contact-us/" , views.contact_us , name="contact.us" ),
    path("search/" , views.search , name="search" ),
    


] 
