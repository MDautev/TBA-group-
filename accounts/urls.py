"""
URL конфигурация за основното приложение.

Този модул дефинира всички URL маршрути за функционалностите на приложението:
- Удостоверяване на потребители (authentication)
- Дашборд изгледи
- Управление на ресторанти

URL Маршрути:
    - Удостоверяване:
        * /login/ - Вход за потребители
        * /logout/ - Изход от системата
        * /register/ - Регистрация на нов потребител
    
    - Дашбордове:
        * /client-dashboard/ - Дашборд за клиенти
        * /employee-dashboard/ - Дашборд за служители на ресторанти
        * /delivery-person-dashboard/ - Дашборд за доставчици
    
    - Управление на ресторанти:
        * /add-restaurant/ - Добавяне на нов ресторант
        * /add-product/ - Добавяне на продукти към ресторанти

Важно:
    Всички URL адреси са именувани (чрез параметъра 'name') за възможност за обратно 
    разрешаване на URL адреси в шаблони и view функции, използвайки:
    - {% url %} template tag
    - reverse() функция

Свързани View функции:
    Съответните view функции за тези URL адреси са дефинирани във views.py в същата директория.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('add-product/', views.add_product, name='add_product'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('delivery-person-dashboard/', views.delivery_person_dashboard, name='delivery_person_dashboard')
]