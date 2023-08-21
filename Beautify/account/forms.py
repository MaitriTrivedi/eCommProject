from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from products.models import Products

class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    contact = forms.CharField(max_length=15)
    password1= forms.CharField(max_length=50,widget=forms.PasswordInput)
    password2= forms.CharField(max_length=50,widget=forms.PasswordInput)

class SellerForm(forms.Form):
    username = forms.CharField(max_length=30)
    company_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    phone = forms.CharField(max_length=15)
    password1= forms.CharField(max_length=50,widget=forms.PasswordInput)
    password2= forms.CharField(max_length=50,widget=forms.PasswordInput)

