from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]