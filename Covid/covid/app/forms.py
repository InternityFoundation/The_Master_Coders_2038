from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User
class ProductForm(forms.ModelForm):
    P_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Product Name',}),required=False)
    P_name = forms.IntegerField(max_digit=4,widget=forms.TextInput(attrs={'placeholder': 'Product quantity',}),required=False)
   