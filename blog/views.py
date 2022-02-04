from unicodedata import category
from django.shortcuts import render
from .models import Post
from shop.models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.core.paginator import Paginator ,  EmptyPage, PageNotAnInteger

# Create your views here.

def all_posts(request):
    posts = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    try:
        posts_ = paginator.page(page)
    except PageNotAnInteger:
        posts_ = paginator.page(1)
    except EmptyPage:
        posts_ = paginator.page(paginator.num_pages)
    categories =  Category.objects.all()
    last_posts = Post.objects.all()[:3]
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "blog-grid.html" , {"posts":posts_ , "categories":categories , "cart":cart , "lp":last_posts})

def get_posts_by_category(request , slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    try:
        posts_ = paginator.page(page)
    except PageNotAnInteger:
        posts_ = paginator.page(1)
    except EmptyPage:
        posts_ = paginator.page(paginator.num_pages)
    categories =  Category.objects.all()
    last_posts = Post.objects.all()[:3]
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "blog-category.html" , {"posts":posts_ , "categories":categories , "cart":cart , "lp":last_posts})



def search(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('title', None)
        posts = Post.objects.all()
        categories = Category.objects.all()
        page = request.GET.get('page', 1)

        last_posts = Post.objects.all()[:3]
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity':item["quantity"],
                "override":True,
            })
        if query_name:
            results = Post.objects.filter(title__contains=query_name)
            paginator = Paginator(results, 6)
            try:
                posts_ = paginator.page(page)
            except PageNotAnInteger:
                posts_ = paginator.page(1)
            except EmptyPage:
                posts_ = paginator.page(paginator.num_pages)
            return render(request, 'search-blog.html', {"posts":posts_ , "categories":categories , "cart":cart , "lp":last_posts})

    return render(request, "search-blog.html")


def post(request , slug):
    post = Post.objects.get(slug=slug)
    categories =  Category.objects.all()

    rel_posts = Post.objects.filter(category=post.category)[:3]
    lp = Post.objects.all()[:3]
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item["quantity"],
            "override":True,
        })
    return render(request , "blog-details.html" , {"post":post , "categories":categories , "cart":cart , "lpp":rel_posts , "lp":lp})
    
    
