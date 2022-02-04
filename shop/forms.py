
from django.db.models import fields
from django.forms.models import model_to_dict
from .models import *
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name" , "description" , "picture","picture2","picture3","amazing_till", "picture4", 'slug','price' , 'available' , 'category'  , "brand","tags", "is_amazing" , "off_price" , "brand")

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("name","slug")

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ("name","slug")

class WebInfoForm(ModelForm):
    class Meta:
        model = WebInfo
        fields = ('banner_1','banner_2','banner_3','banner_4','small_banner_1','small_banner_2','footertext',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

class ProductSizesForm(ModelForm):
    class Meta:
        model = ProductSizes
        fields = ("name" , "price" , "off_price" , "picture" , )