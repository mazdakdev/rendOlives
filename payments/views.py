
from django.shortcuts import render , get_object_or_404

# Create your views here.
import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from cart.forms import CartAddProductForm
from orders.models import Order
from shop.models import Product
from orders.models import OrderItems
from orders.tasks import order_created
from cart.cart import Cart

def go_to_gateway_view(request ):
    order_id_ = request.session.get("order_id")
    print(order_id_)
    order = get_object_or_404(Order , id=order_id_)
    #total_price = order.get_total_cost()
    #print(total_price)
    # خواندن مبلغ از هر جایی که مد نظر است
    #total_price
    if order.method == "ارسال رایگان" or order.method == "تیپاکس":
        amount = order.get_total_cost()
    else:
        amount = order.get_total_cost() + 50000

    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = order.phone_num # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.ZARINPAL) # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e



def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404 

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        order_id = request.session.get("order_id")
        order = get_object_or_404(Order , id=order_id)
        order.is_paid = True
        order.save()
   
        order_created.delay(order.id)
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        #order_id = request.session.get("order_id")
        #order = get_object_or_404(Order , id=order_id)
        return render(request,"order-created.html",{"order":order ,"cart":cart})

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order , id=order_id)
    order.status = "لغو شده"
    order.save()
    return render(request,"order-failed.html",{"order":order ,"cart":cart})