
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Restaurant, Product
from django import forms
from .models import Order, OrderItem, Product

"""
Форми за създаване и управление на потребители, ресторанти и продукти.

Съдържа:
- CustomUserCreationForm: форма за регистрация с избор на роля.
- RestaurantForm: форма за създаване/редакция на ресторанти.
- ProductForm: форма за създаване/редакция на продукти.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Restaurant, Product



class CustomUserCreationForm(UserCreationForm):
    """
    Разширена форма за регистрация на потребител с избор на роля.

    Позволява избор между клиент, служител или доставчик по време на регистрация.

    Attributes:
        role (ChoiceField): Избор на тип потребител.
    """
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('employee', 'Служител'),
        ('delivery_person', 'Доставчик'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роля')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


class RestaurantForm(forms.ModelForm):
    """
    ModelForm за създаване и редактиране на ресторанти.

    Свързана директно с модела Restaurant.
    """
    class Meta:
        model = Restaurant
        fields = ['name', 'address']


class ProductForm(forms.ModelForm):
    """
    ModelForm за създаване и редактиране на продукти.

    Свързана директно с модела Product.
    """
    class Meta:
        model = Product

        fields = ['restaurant', 'name', 'description', 'price', 'category']



class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['items']

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, required=True, label="Адрес")
    phone_number = forms.CharField(max_length=20, required=True, label="Телефонен номер")



        fields = ['restaurant', 'name', 'description', 'price']

