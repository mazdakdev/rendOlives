from email import message
from pprint import pprint
from celery import shared_task
from django.core.mail import send_mail
from .models import Order , OrderItems
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItems.objects.filter(order = order)
    subject = f"{order.user.first_name} عزیز سفارش شما به کد #{order.order_id} ثبت شد"
    html_message = render_to_string('letter.html' , {"order":order , "order_items":order_items })
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject , plain_message , "info@rendolives.ir" , [order.email] , html_message=html_message)
    mobile = order.user.mobile
    token = "aXw9ZVWoxzv9wIanoN95x-SwibOTrmtLALSlcbA_9jc="
    pid = "frobbc6bgy"
    fnum = "+985000125475"
    p1 = "name" 
    v1 = order.first_name
    p2 = "order_id"
    v2 = order.order_id
    requests.get(f"http://ippanel.com:8080/?apikey={token}&pid={pid}&fnum={fnum}&tnum={mobile}&p1={p1}&v1={v1}&p2={p2}&v2={v2}")
    if order.method == "ارسال رایگان" or order.method == "تیپاکس":
        amount = order.get_total_cost()
    else:
        amount = order.get_total_cost() + 50000
    

    oid = str(order.order_id)
    requests.get(f"http://ippanel.com:8080/?apikey={token}&pid=ds6io4te7j&fnum={fnum}&tnum=09981483416&p1=name&v1=مهدی&p2=order_id&v2={oid}&p3=price&v3={amount}")
    return mail_sent


