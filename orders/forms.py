from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("first_name" , "last_name" , "email" , "company" , "city" , "ostan" , "postal_code" , "extra_desc" , "country" , "address"  , "method" , "phone_num" )