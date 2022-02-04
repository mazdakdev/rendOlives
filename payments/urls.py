from urllib.parse import urlparse
from django.urls import path
from . import views
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-getway/', views.go_to_gateway_view , name="pay"),
    path('callback-getway/', views.callback_gateway_view , name="callback-gateway"),
]
