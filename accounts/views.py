from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import *
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Product
from .forms import RestaurantForm, ProductForm

# Create your views here.

def register(request):
    """
    Обработва регистрация на потребители с определяне на роли.
    
    Обработва регистрационната форма и създава потребители с определени роли:
    - Клиент
    - Служител
    - Доставчик
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponseRedirect: Пренасочва към страница за вход при успех
        HttpResponse: Показва регистрационна форма при GET или невалиден POST
        
    Поведение:
        - При POST заявки:
            * Валидира CustomUserCreationForm
            * Задава роля на потребителя според избора във формата
            * Създава клиентски профил ако потребителят е клиент
            * Показва съобщение за успех
            * Пренасочва към страница за вход
        - При GET заявки:
            * Показва празна регистрационна форма
            
    Съобщения:
        - Успех: Потвърждение за създаване на акаунт
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            if role == 'client':
                user.is_client = True
            elif role == 'employee':
                user.is_employee = True
            elif role == 'delivery_person':
                user.is_delivery_person = True
            user.save()
            if user.is_client:
                Client.objects.create(user=user, address='Default Address')
            messages.success(request, f'Акаунтът за {user.username} е създаден успешно!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    """
    Обработва удостоверяване на потребител и пренасочване според ролята.
    
    Обработва формата за вход и пренасочва потребителите към съответния дашборд
    според тяхната роля след успешно удостоверяване.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponseRedirect: Пренасочва към съответния дашборд
        HttpResponse: Показва форма за вход при GET или невалиден POST
        
    Пренасочвания:
        - Клиенти → client_dashboard
        - Служители → employee_dashboard
        - Доставчици → delivery_person_dashboard
        - Други → home
        
    Използва:
        - Вградената AuthenticationForm на Django
        - auth_login() за създаване на сесия
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Влизане в системата
            if user.is_client:
                return redirect('client_dashboard')  # Пренасочване към клиентския дашбоард
            elif user.is_employee:
                return redirect('employee_dashboard')  # Пренасочване към дашбоарда за служители
            elif user.is_delivery_person:
                return redirect('delivery_person_dashboard')  # Пренасочване към дашбоарда за доставчици
            else:
                return redirect('home')  # Резервен вариант, ако ролята не е зададена
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    """
    Обработва излизане от системата.
    
    Приключва текущата потребителска сесия и пренасочва към страница за вход.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponseRedirect: Пренасочва към страница за вход
        
    Съобщения:
        - Успех: Съобщение за потвърждение на изход
    """
    auth_logout(request)
    messages.success(request, 'Успешно излязохте.')
    return redirect('login')

def home(request):
    """
    Показва началната страница на приложението.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponse: Показва home.html шаблон
    """
    return render(request, 'accounts/home.html')

@login_required
def add_restaurant(request):
    """
    Обработва създаване на ресторант (само за служители).
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponseRedirect: Пренасочва към дашборда на служители при успех
        HttpResponse: Показва форма при GET или невалиден POST
        
    Контрол на достъпа:
        - Изисква вписване (@login_required)
        - Ограничено до служители (ръчна проверка)
        
    Поведение:
        - Пренасочва не-служители към начална страница
        - Валидира RestaurantForm
        - Запазва нов ресторант при валидна форма
    """
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да добавят ресторанти
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'accounts/add_restaurant.html', {'form': form})

@login_required
def add_product(request):
    """
    Обработва създаване на продукти за ресторанти (само за служители).
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponseRedirect: Пренасочва към дашборда на служители при успех
        HttpResponse: Показва форма при GET или невалиден POST
        
    Контрол на достъпа:
        - Изисква вписване (@login_required)
        - Ограничено до служители (ръчна проверка)
        
    Използва:
        - ProductForm за валидация и запазване
    """
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да добавят продукти
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = ProductForm()
    return render(request, 'accounts/add_product.html', {'form': form})

def client_dashboard(request):
    """
    Показва дашборда за клиенти.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponse: Показва client_dashboard.html шаблон
        
    Бележка:
        Обикновено би включвал данни специфични за клиенти
    """
    return render(request, 'accounts/client_dashboard.html')

def employee_dashboard(request):
    """
    Показва дашборда за служители.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponse: Показва employee_dashboard.html шаблон
        
    Бележка:
        Обикновено би включвал данни специфични за служители
    """
    return render(request, 'accounts/employee_dashboard.html')

def delivery_person_dashboard(request):
    """
    Показва дашборда за доставчици.
    
    Аргументи:
        request (HttpRequest): Обектът на HTTP заявката
        
    Връща:
        HttpResponse: Показва delivery_person_dashboard.html шаблон
        
    Бележка:
        Обикновено би включвал данни специфични за доставчици
    """
    return render(request, 'accounts/delivery_person_dashboard.html')
