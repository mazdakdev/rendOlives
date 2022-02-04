from django.shortcuts import  get_object_or_404 , redirect , render
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product, ProductSizes
from .forms import CartAddProductForm

@require_POST
def cart_add(request , product_id , size):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    if size != 0:
        size_ = product.size.get(id=size)
    else:
        size_ = None

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product , quantity=cd['quantity'] ,size_=size_, override_quantity=cd['override'] )
    return redirect("home")

@require_POST
def cart_remove(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product=product)
    return redirect("cart.detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "cart.html" , {"cart":cart})

