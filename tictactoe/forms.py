from django import forms
from .models import *

from django.db.models import fields
from django.forms import ModelForm

# Creating form for registration
class Registration(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Retype Password'}))


# Log in form
class Log_in(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class Change_pass(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Existed password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_pass_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password repeat'}))

player = (
    ("X", "X"),
    ("O", "O")
)
  
# creating a form 
class Player(forms.Form):
    player_as = forms.ChoiceField(choices = player)
    

