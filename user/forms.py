from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import OrderAddress
from .models import MyUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['mobile', ]

class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = ( "company" , "city" , "ostan" , "postal_code"  , "country" , "address" , "phone_num"  )

