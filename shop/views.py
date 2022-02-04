
import imp
from django.contrib.auth import login
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from user.views import categories, product
from .models import Category, Comment, Product , Brand 
from .models import WebInfo as wb
from .forms import CommentForm, WebInfoForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.db.models import Q
from blog.models import Post


# Create your views here.
def HomeView(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('-id')[:5]
    off_products = Product.objects.filter(~Q(off_price=None))
    posts = Post.objects.all().order_by('-id')[:7]
    info = wb.objects.get(id=1)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "index.html" , {"categories":categories,"products":products , "posts":posts ,"off_products":off_products, "info":info , "cart":cart })


@login_required
def WebInfo(request):
    info = wb.objects.get(id=1)
    if request.method == "POST":
        form = WebInfoForm(request.POST , request.FILES , instance=info )
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
         
    return render(request, 'dashboard/web-info.html', {'info': info})

def get_product_by_category(request , slug):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    category = get_object_or_404(Category, slug = slug)
    products = Product.objects.filter(category = category , available=True)
    info = wb.objects.get(id=1)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "shop-category.html" , {"products":products , "categories":categories ,"brands":brands, "info":info , "cart":cart})

def get_product_by_brand(request , slug):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    brand = get_object_or_404(Brand, slug = slug)
    products = Product.objects.filter(brand = brand , available=True)
    info = wb.objects.get(id=1)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })

    return render(request , "shop-brand.html" , {"products":products , "categories":categories ,"brands":brands,"cart":cart, "info":info})

def get_product_by_slug(request , slug):
    product = Product.objects.get(slug=slug)
    similar_products = Product.objects.filter(category = product.category.id , available=True)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "product-details.html" , {"product":product , "smproducts":similar_products , "cart":cart})


@login_required
def add_comment(request , slug):
    product = get_object_or_404(Product , slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.product = product
            f.user = request.user
            f.save()
            return redirect("get.single.product" ,product.slug)

def shop(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    form_ = CartAddProductForm()
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "shop.html" , {"products":products , "categories":categories , "brands":brands , "form_":form_ , "cart":cart})


def about_us(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "about-us.html" , {"cart":cart})


def contact_us(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "contact-us.html" , {"cart":cart})


def search(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        form_ = CartAddProductForm()
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity':item["quantity"],
                "override":True,
            })
        if query_name:
            results = Product.objects.filter(name__contains=query_name)
            return render(request, 'search.html', {"results":results , "products":products , "categories":categories , "brands":brands , "form_":form_ , "cart":cart})

    return render(request, "search.html")
