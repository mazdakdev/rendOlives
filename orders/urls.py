from django.urls import path
from . import views

urlpatterns = [
    path("order-created" , views.order_create , name="order.create"),

]
