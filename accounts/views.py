from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import *
from .forms import CustomUserCreationForm, CheckoutForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RestaurantForm, ProductForm
from .models import Restaurant, Product
from .forms import OrderForm

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

@login_required
def employee_dashboard(request):

    if not request.user.is_employee:
        return redirect('home')
    restaurants = Restaurant.objects.all()
    products = Product.objects.all()
    return render(request, 'accounts/employee_dashboard.html', {
        'restaurants': restaurants,
        'products': products,
    })

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

@login_required
def edit_restaurant(request, pk):
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да редактират ресторанти
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'accounts/edit_restaurant.html', {'form': form})

@login_required
def delete_restaurant(request, pk):
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да изтриват ресторанти
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('employee_dashboard')
    return render(request, 'accounts/delete_restaurant.html', {'restaurant': restaurant})

@login_required
def edit_product(request, pk):
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да редактират продукти
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('employee_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'accounts/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    if not request.user.is_employee:
        return redirect('home')  # Само служители могат да изтриват продукти
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('employee_dashboard')
    return render(request, 'accounts/delete_product.html', {'product': product})

@login_required
def view_products(request):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да правят поръчки

    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    categories = Product.CATEGORY_CHOICES  # Всички налични категории

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)

        # Добавяне или актуализиране на продукта в количката
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = quantity  # Ако е нов запис, задаваме количеството
        else:
            cart_item.quantity += quantity  # Ако вече съществува, увеличаваме количеството
        cart_item.save()

        return redirect('view_products')

    return render(request, 'accounts/view_products.html', {'products': products, 'categories': categories})


@login_required
def delivery_dashboard(request):
    if not request.user.is_delivery_person:
        return redirect('home')  # Само доставчици могат да виждат този дашбоард

    # Филтриране на поръчки според статуса
    orders = Order.objects.filter(status__in=['pending', 'shipped']).order_by('-created_at')

    return render(request, 'accounts/delivery_dashboard.html', {'orders': orders})


@login_required
def accept_delivery(request, pk):
    if not request.user.is_delivery_person:
        return redirect('home')  # Само доставчици могат да приемат доставки

    order = get_object_or_404(Order, pk=pk)
    if order.status == 'pending':
        order.status = 'shipped'
        order.delivery_person = request.user
        order.save()
    return redirect('delivery_dashboard')


@login_required
def create_order(request):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да правят поръчки

    # Филтриране на продукти според категорията
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    categories = Product.CATEGORY_CHOICES  # Всички налични категории

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = Client.objects.get(user=request.user)

            # Изчисляване на общата цена на поръчката
            total_price = 0
            for item in form.cleaned_data['items']:
                quantity = int(request.POST.get(f'quantity_{item.id}', 1))  # Вземаме количеството от заявката
                price = item.price * quantity
                total_price += price

            order.total_price = total_price
            order.save()

            # Създаване на OrderItem записи
            for item in form.cleaned_data['items']:
                quantity = int(request.POST.get(f'quantity_{item.id}', 1))
                OrderItem.objects.create(
                    order=order,
                    product=item,
                    quantity=quantity,
                    price=item.price * quantity
                )

            # Пренасочване към страницата за финализиране на поръчка
            return redirect('checkout', order_id=order.pk)
    else:
        form = OrderForm()
    return render(request, 'accounts/create_order.html', {'form': form, 'products': products, 'categories': categories})

@login_required
def mark_as_delivered(request, pk):
    if not request.user.is_delivery_person:
        return redirect('home')  # Само доставчици могат да маркират доставки

    order = get_object_or_404(Order, pk=pk)
    if order.delivery_person == request.user and order.status == 'shipped':
        order.status = 'delivered'
        order.save()
    return redirect('delivery_dashboard')

@login_required
def add_to_cart(request, pk):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да добавят продукти в количката
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_products')
@login_required
def view_cart(request):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да правят поръчки
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'accounts/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, pk):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да премахват продукти от количката
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да правят поръчки

    client = Client.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

            # Създаване на поръчка
            order = Order.objects.create(
                client=client,
                total_price=sum(item.product.price * item.quantity for item in cart_items),
                status='pending',
                address=address,
                phone_number=phone_number
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price * item.quantity
                )
            cart_items.delete()  # Изчистваме количката
            return redirect('client_dashboard')
    else:
        form = CheckoutForm()
    return render(request, 'accounts/checkout.html', {'form': form})

@login_required
def track_orders(request):
    if not request.user.is_client:
        return redirect('home')  # Само клиенти могат да проследяват поръчки
    client = Client.objects.get(user=request.user)
    orders = Order.objects.filter(client=client).order_by('-created_at')
    return render(request, 'accounts/track_orders.html', {'orders': orders})
