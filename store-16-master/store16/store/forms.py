from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

  
class ProductForm(forms.ModelForm):   
    class Meta: 
        model = Product
        fields = ['title', 'author', 'publisher','subject', 'genre', 'series', 'isbn', 'image', 'abstract'] 

class SearchForm(forms.Form):
	q = forms.CharField(label='Search', max_length=50)