from email import message
from pprint import pprint
from django.core.mail import send_mail
from orders.models import Order , OrderItems
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
import requests

@shared_task
def order_status_changed(order_id , status_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItems.objects.filter(order = order)
    if status_id == 1:
        status = "در حال انجام"
    elif status_id == 2:
        status = "تکمیل شده"
    elif status_id == 3:
        status = "لغو شده"
    elif status_id == 4:
        status = "معلق"

    subject = f"{order.user.first_name} عزیز سفارش شما به کد #{order.order_id} به حالت {status} در آمد"
    html_message = render_to_string('letter-change.html' , {"order":order , "order_items":order_items , "status":status })
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject , plain_message , "info@rendolives.ir" , [order.email] , html_message=html_message)
    mobile = order.user.mobile
    token = "aXw9ZVWoxzv9wIanoN95x-SwibOTrmtLALSlcbA_9jc="
    pid = "9n4ux76rci"
    fnum = "+9810004223"
    p1 = "order_id" 
    v1 = str(order.order_id)
    p2 = "status"
    v2 = status
    requests.get(f"http://ippanel.com:8080/?apikey={token}&pid={pid}&fnum={fnum}&tnum={mobile}&p1={p1}&v1={v1}&p2={p2}&v2={v2}")
    return mail_sent


    