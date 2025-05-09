
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



'''
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
        fields = ('username', 'password1', 'password2', 'role')  # Добавяме полето "role"

'''
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('client', 'Клиент'),
            ('employee', 'Служител'),
            ('delivery_person', 'Доставчик'),
        ],
        widget=forms.RadioSelect,
        required=True,
    )

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
    """
    Форма за създаване и редактиране на поръчки с включени продукти.

    Предоставя интерфейс с checkbox-и за избор на множество продукти,
    които да бъдат включени в поръчката. Обслужва many-to-many връзката
    между Order и Product.

    Полета:
        items (ModelMultipleChoiceField):
            - Позволява избор на множество продукти
            - Визуализира се като checkbox-и (CheckboxSelectMultiple)
            - Задължително поле (трябва да изберете поне един продукт)
            - Съдържа всички налични продукти от базата данни

    Meta:
        model (Order): Моделът Order, на който се базира формата
        fields (list): Съдържа само полето 'items', което е единственото
                      необходимо за създаване на поръчка

    Примерна употреба:
        form = OrderForm()
        # или със съществуваща поръчка
        form = OrderForm(instance=поръчка)
        
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=поръчка)
            if form.is_valid():
                поръчка = form.save()
                # Допълнителна обработка...

    Валидация:
        - Автоматично проверява дали избраните продукти съществуват
        - Изисква избор на поне един продукт

    Рендиране в шаблони:
        Показва checkbox-и за избор на продукти. В шаблона използвайте:
        {% for checkbox in form.items %}
            {{ checkbox.tag }} {{ checkbox.choice_label }}
        {% endfor %}
    """
    items = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['items']

class CheckoutForm(forms.Form):
    """
    Форма за финализиране на поръчка и въвеждане на данни за доставка.

    Полета:
        address (CharField):
            - Адрес за доставка
            - Максимална дължина: 255 символа
            - Задължително поле
            - Етикет: "Адрес"

        phone_number (CharField):
            - Телефонен номер за връзка
            - Максимална дължина: 20 символа
            - Задължително поле
            - Етикет: "Телефонен номер"

    Валидация:
        - Проверява дали е въведен адрес
        - Проверява формата на телефонния номер
        - Автоматично премахва празните пространства от полетата

    Примерна употреба:
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            адрес = form.cleaned_data['address']
            телефон = form.cleaned_data['phone_number']
            # Създаване на поръчка...

    Забележки:
        - Това е стандартна Django форма (не ModelForm)
        - Не включва логика за плащане
        - Полетата ['restaurant', 'name', 'description', 'price'] са документирани,
          но не са част от текущата версия на формата
    """
    address = forms.CharField(max_length=255, required=True, label="Адрес")
    phone_number = forms.CharField(max_length=20, required=True, label="Телефонен номер")

class DateRangeForm(forms.Form):
    """
    Форма за избор на период от дати.

    Полета:
        start_date (DateField): Начална дата на периода. Визуализира се като HTML елемент от тип 'date'.
        end_date (DateField): Крайна дата на периода. Визуализира се като HTML елемент от тип 'date'.
    """
    start_date = forms.DateField(
        label="От дата",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label="До дата",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
