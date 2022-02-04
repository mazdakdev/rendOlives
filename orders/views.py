from cmath import cos
from http.client import HTTPResponse
from statistics import quantiles
from django.shortcuts import render , redirect

from cart.forms import CartAddProductForm
from .forms import OrderCreateForm
from .models import OrderItems , Order
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from user.models import MyUser as User
from pprint import pprint
from .tasks import order_created
from django.urls import reverse
from user.models import OrderAddress
from django.core.exceptions import ObjectDoesNotExist

@login_required
def order_create(request):
    cart = Cart(request)
    user = User.objects.get(id=request.user.id)
    try:
        address = OrderAddress.objects.get(user=request.user)
    except ObjectDoesNotExist:
        address = None
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for i in cart:
                OrderItems.objects.create(order=order , product = i["product"] , price= i['price'] , quantity=i["quantity"] )
            cart.clear()
            


            #return render(request , "order-created.html" , {"order":order })
           
            request.session['order_id'] = order.id
            print(f"order : {order.id}")
            return redirect(reverse("pay"))
        else:
            print(form.errors)
    else:
        form = OrderCreateForm()
    return render(request , "order-create.html" , {"form":form , 'cart':cart , "user":user  , "address":address})
 



