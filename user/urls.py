from django.urls import path , include
from . import views
from shop import views as sview
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('signin/', views.register_view, name='signin'),
    path('verify/', views.verify, name='verify'),

    path('profile/', views.profile, name='profile'),
    path('products-list/', views.products, name='admin.products'),
    path('product/<int:id>', views.product, name='admin.product'),
    path('delete-product/<int:id>', views.delete_product, name='admin.product.delete'),
    path("update-product/<int:id>" , views.update_product , name="admin.product.update"),
    path("create-product/" , views.create_product , name="admin.product.create"),
    path("categories/" , views.categories , name="admin.categories"),
    path("delete-category/<int:id>" , views.delete_category , name="admin.category.delete"),
    path("update-category/<int:id>" , views.edit_category , name="admin.category.update"),
    path("create-size/<int:product_id>" , views.create_size , name="admin.size.create"),
    path("create-category/" , views.create_category , name="admin.category.create"),
    path("webinfo/" , sview.WebInfo , name="web.info"),
    path("comments/" , views.comments , name="admin.comments"),
    path("brands/" , views.brands , name="admin.brands"),
    path("delete-brand/<int:id>" , views.delete_brand , name="admin.delete.brand"),
    path("update-brand/<int:id>" , views.update_brand , name="admin.update.brand"),
    path("create-brand/" , views.create_brand , name="admin.create.brand"),
    path("comments/<int:id>/delete/" , views.delete_comment , name="admin.delete.comment"),
    path("orders/<int:order_id>/delete/" , views.remove_order , name="admin.delete.order"),
    path("orders/<int:order_id>/change-order-status-to/<int:status_id>" , views.change_order_status , name="admin.change.order"),
    path("order-history/<int:order_id>" , views.get_order_items_by_id , name="get.order.item"),
    path("orders/" , views.orders , name="orders"),
    path("search/" , views.search , name="search.order"),
    path("posts/" , views.posts , name="user.posts"),
    path("post/<int:id>" , views.post , name="admin.post"),
    path("post-delete/<int:id>" , views.delete_post , name="admin.post.delete"),
    path("post-update/<int:id>" , views.update_post , name="admin.post.update"),
    path("add-post/" , views.add_post , name="admin.post.create"),
    path("orders/<int:id>" , views.order_items , name="admin.order"),
    path("product/<int:id>/sizes/" , views.sizes , name="admin.sizes"),
    path("delete-size/<int:id>" , views.del_size , name="del.size"),
    path("edit-size/<int:id>" , views.edit_size , name="edit.size"),


  
]