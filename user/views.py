from importlib.metadata import requires
from pprint import pprint
from pydoc import render_doc
from unicodedata import category

from urllib import request
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from user.models import OrderAddress
from .forms import OrderAddressForm
from shop.models import Brand, Comment, Product , Category, ProductSizes 
from orders.models import Order, OrderItems
from shop.models import WebInfo as wb
from shop.forms import BrandForm, CommentForm, ProductForm , CategoryForm, ProductSizesForm
from .tasks import order_status_changed
from django.db.models import Q
from azbankgateways.models import Bank
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.core.exceptions import ObjectDoesNotExist
from blog.models import Post
from blog.forms import PostForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import MyUser
from .models import MyUser as User
from . import forms
from . import helper
from django.contrib import messages



def register_view(request):
    form = forms.RegisterForm

    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                print(mobile)
                user = MyUser.objects.get(mobile=mobile)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))

        except MyUser.DoesNotExist:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'register.html', {'form': form})


def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile = mobile)

        if request.method == "POST":

            # check otp expiration
            if not helper.check_otp_expiration(user.mobile):
                messages.error(request, "کد ارسال شده منقضی شده است لطفا دوباره اقدام کنید")
                return HttpResponseRedirect(reverse('signin'))

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "کد وارد شده اشتباه است")
                return HttpResponseRedirect(reverse('signin'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))

        return render(request, 'verify.html', {'mobile': mobile})

    except MyUser.DoesNotExist:
        messages.error(request, "مشکلی پیش آمد لطفا دوباره امتحان کنید")
        return HttpResponseRedirect(reverse('signin'))




def get_cost(self):
    return self.quantity * self.price


@login_required
def profile(request):
    if request.user.is_superuser:
        orders = Order.objects.filter(is_paid=True)
        user_count = User.objects.all().count()
        current_orders = Order.objects.filter(is_paid=True )

        payments = Bank.objects.all().order_by('-id')[:7]



        return render(request, 'dashboard/app-profile.html' , {"orders":orders , "user_count":user_count , 'current_orders':current_orders ,  "payments":payments })
    else:
        orders_ = Order.objects.filter(user=request.user)
        try:
            address = OrderAddress.objects.get(user=request.user)
        except ObjectDoesNotExist:
            address = None
            
        if request.method == "POST":
            form = OrderAddressForm(request.POST , instance=address)
            if form.is_valid():
                f=form.save(commit=False)
                f.user = request.user
                f.save()
            else:
                print(form.errors)
            return redirect("profile")
        else:
            
            return render(request , "my-account.html" , {"items" : orders_ , "address":address} )



@login_required
def products(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        return render(request , "dashboard/admin-products.html" , {"products":products})

@login_required
def product(request , id):
    if request.user.is_superuser:
        product = Product.objects.get(id=id)
        comment_count = Comment.objects.filter(product=product).count()

        return render(request , "dashboard/admin-product.html" , {"product":product , "count":comment_count})

@login_required
def delete_product(request , id):
    if request.user.is_superuser:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect("admin.products")

@login_required
def update_product(request , id):
    if request.user.is_superuser:
        categories = Category.objects.all()
        product = Product.objects.get(id=id)
        brands = Brand.objects.all()
        if request.method == "POST":
            form = ProductForm(request.POST , request.FILES , instance=product)
            if form.is_valid():
                form.save()
                return redirect("admin.products")
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, 'dashboard/admin-update-product.html',{'form':form})

        return render(request , "dashboard/admin-update-product.html" , {"product":product , "categories":categories , "brands":brands})

@login_required
def create_product(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        brands = Brand.objects.all()
        if request.method == "POST":
            form = ProductForm(request.POST , request.FILES)
            if form.is_valid():
                form.save()
                return redirect("admin.size.create" , form.instance.id)
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, 'dashboard/admin-create-product.html',{'form':form})
        return render(request , "dashboard/admin-create-product.html" , {"categories":categories,"brands":brands})

@login_required
def create_size(request , product_id):
    if request.user.is_superuser:
        product = Product.objects.get(id=product_id)
        if request.method == "POST":
            form = ProductSizesForm(request.POST , request.FILES)
            if form.is_valid():
                f = form.save(commit=False)
                f.product = product
                f.save()
                return redirect("admin.size.create" ,  product.id)
            else:
                return render(request , 'dashboard/add-size.html' , {"form":form, "product":product})
        return render(request , 'dashboard/add-size.html' , {"product":product})
        

@login_required
def categories(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        return render(request,"dashboard/categories.html"  , {"categories":categories})

@login_required
def delete_category(request , id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect("admin.categories")

@login_required
def edit_category(request , id):
    if request.user.is_superuser:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            form = CategoryForm(request.POST  , instance=category)
            if form.is_valid():
                form.save()
                return redirect("admin.categories")
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, 'dashboard/update-category.html',{'form':form})

        return render(request , "dashboard/update-category.html" , {"category":category})

@login_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin.categories")
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, 'dashboard/create-category.html',{'form':form})
    return render(request , "dashboard/create-category.html" )


@login_required
def comments(request):
    if request.user.is_superuser:
        comments = Comment.objects.all()
        return render(request , "dashboard/admin-comments.html" , {"comments" : comments})

@login_required
def delete_comment(request , id):
    if request.user.is_superuser:
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect("admin.comments")

@login_required()
def brands(request):
    if request.user.is_superuser:
        brands = Brand.objects.all()
        return render(request, "dashboard/admin-brands.html" , {"brands":brands} )

@login_required()
def delete_brand(request, id ):
    if request.user.is_superuser:
        brand = Brand.objects.get(id=id)
        brand.delete()
        return redirect("admin.brands")


@login_required
def update_brand(request , id):
    if request.user.is_superuser:
        brand = Brand.objects.get(id=id)
        if request.method == "POST":
            form = BrandForm(request.POST  , instance=brand)
            if form.is_valid():
                form.save()
                return redirect("admin.brands")
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, 'dashboard/update-brand.html',{'form':form})

        return render(request , "dashboard/update-brand.html" , {"brand":brand})

@login_required
def create_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin.brands")
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, 'dashboard/create-brand.html',{'form':form})
    return render(request , "dashboard/create-brand.html" )


@login_required
def remove_order(request , order_id):
    if request.user.is_superuser:
        order = Order.objects.get(id=order_id)
        order.delete()
        return redirect("profile")


@login_required
def change_order_status(request , status_id , order_id):
    order = Order.objects.get(id=order_id)
    if request.user.is_superuser:
        if status_id == 1:
            order.status = "در حال انجام"
            order.save()
            order_status_changed.delay(order.id , 1 )
        elif status_id == 2:
            order.status = "تکمیل شده"
            order.save()
            order_status_changed.delay(order.id , 2 )
        elif status_id == 3:
            order.status = "لغو شده"
            order.save()
            order_status_changed.delay(order.id , 3 )
            
        elif status_id == 4:
            order.status = "معلق"
            order.save()
            order_status_changed.delay(order.id , 4 )
        else:
            pass

        return redirect("orders")

@login_required
def get_order_items_by_id(request , order_id):
    order = get_object_or_404(Order , id=order_id)
    orders = OrderItems.objects.filter(order=order)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "orders.html" , {"orders":orders , "o":order , "cart":cart})
    

@login_required
def orders(request):
    if request.user.is_superuser:
        orders = Order.objects.filter
        return render(request, 'dashboard/orders.html' , {"orders":orders})

@login_required
def search(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        print(query_name)
        if query_name:
            results = Order.objects.filter(order_id__contains=query_name)
            return render(request, 'dashboard/orders.html', {"results":results})

    return render(request, "dashboard/orders.html")

@login_required
def posts(request):
    if request.user.is_superuser:
        posts = Post.objects.all()
        return render(request , "dashboard/posts.html" , {"posts":posts})

@login_required
def post(request ,id ):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        return render(request , "dashboard/post.html" , {"post":post})


@login_required
def delete_post(request ,id ):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        post.delete()
        return redirect("user.posts")

    
@login_required
def update_post(request ,id ):
    if request.user.is_superuser:
        post = Post.objects.get(id=id)
        categories = Category.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST , request.FILES , instance=post)
            if form.is_valid():
                form.save()
                return redirect("user.posts")
            else:
                return render(request, 'dashboard/update-post.html',{'form':form , "categories":categories})
        return render(request , "dashboard/update-post.html" , {"post":post , "categories":categories})



@login_required
def add_post(request ):
    if request.user.is_superuser:
        categories = Category.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST , request.FILES )
            if form.is_valid():
                form.save()
                return redirect("user.posts")
            else:
                return render(request, 'dashboard/add-post.html',{'form':form , "categories":categories})
        return render(request , "dashboard/add-post.html" , {"post":post , "categories":categories})




def order_items(request , id):
    order = get_object_or_404(Order , id=id)
    orders = OrderItems.objects.filter(order=order)
    return render(request , 'dashboard/order-items.html' , {'orders':orders , "o":order})



def sizes(request , id):
    product = Product.objects.get(id=id)
    sizes = ProductSizes.objects.filter(product=product)

    return render(request,"dashboard/sizes.html" , {"sizes":sizes})


def del_size(request , id):
    size = ProductSizes.objects.get(id=id)
    size.delete()
    return redirect("admin.sizes" , size.product.id)

def edit_size(request , id):
    if request.user.is_superuser:
        size = ProductSizes.objects.get(id=id)
        product = size.product
        if request.method == "POST":
            form = ProductSizesForm(request.POST , request.FILES , instance=size)
            if form.is_valid():
                f = form.save(commit=False)
                f.product = product
                f.save()
                return redirect("admin.sizes" ,  product.id)
            else:
                return render(request , 'dashboard/edit-size.html' , {"form":form, "product":product , "size":size})
        return render(request , 'dashboard/edit-size.html' , {"product":product , "size":size})
    