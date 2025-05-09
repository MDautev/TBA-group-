"""
URL конфигурация за основното приложение.

Този модул дефинира всички URL маршрути за основните функционалности на приложението, включително:
- Удостоверяване на потребители
- Дашборд изгледи
- Управление на ресторанти и продукти
- Управление на поръчки и доставки

URL Маршрути:
    - Удостоверяване:
        * /login/ - Вход за потребители
        * /logout/ - Изход от системата
        * /register/ - Регистрация на нов потребител
    
    - Дашбордове:
        * /client-dashboard/ - Дашборд за клиенти
        * /employee-dashboard/ - Дашборд за служители на ресторанти
        * /delivery-person-dashboard/ - Дашборд за доставчици
        * /admin-dashboard/ - Дашборд за администратори
    
    - Управление на ресторанти:
        * /add-restaurant/ - Добавяне на нов ресторант
        * /edit-restaurant/<int:pk>/ - Редактиране на ресторант
        * /delete-restaurant/<int:pk>/ - Изтриване на ресторант
    
    - Управление на продукти:
        * /add-product/ - Добавяне на продукт към ресторант
        * /edit-product/<int:pk>/ - Редактиране на продукт
        * /delete-product/<int:pk>/ - Изтриване на продукт
        * /view-products/ - Преглед на всички продукти
    
    - Управление на поръчки:
        * /create-order/ - Създаване на нова поръчка
        * /add-to-cart/<int:pk>/ - Добавяне на продукт в кошницата
        * /remove-from-cart/<int:pk>/ - Премахване на продукт от кошницата
        * /view-cart/ - Преглед на кошницата
        * /checkout/ - Плащане на поръчката
        * /track-orders/ - Преглед на състоянието на поръчките

    - Доставки:
        * /delivery-dashboard/ - Дашборд за доставчици
        * /accept-delivery/<int:pk>/ - Приемане на доставка
        * /mark-as-delivered/<int:pk>/ - Маркиране на поръчка като доставена

    - Отчети:
        * /turnover-report/ - Отчет за оборота
        * /generate-turnover-report/ - Генериране на отчет за оборота
        * /earnings-report/ - Отчет за печалбите

Всички URL адреси са именувани (чрез параметъра 'name') за възможност за обратно разрешаване на URL адреси в шаблони и view функции, използвайки:
    - {% url %} template tag
    - reverse() функция

Свързани View функции:
    Съответните view функции за тези URL адреси са дефинирани във views.py в същата директория.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Основни маршрути
    path('', views.home, name='home'),

    # Удостоверяване
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    # Дашбордове
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('delivery-person-dashboard/', views.delivery_person_dashboard, name='delivery_person_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Управление на ресторанти
    path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    path('edit-restaurant/<int:pk>/', views.edit_restaurant, name='edit_restaurant'),
    path('delete-restaurant/<int:pk>/', views.delete_restaurant, name='delete_restaurant'),

    # Управление на продукти
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('view-products/', views.view_products, name='view_products'),

    # Управление на поръчки
    path('create-order/', views.create_order, name='create_order'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('track-orders/', views.track_orders, name='track_orders'),

    # Доставки
    path('delivery-dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('accept-delivery/<int:pk>/', views.accept_delivery, name='accept_delivery'),
    path('mark-as-delivered/<int:pk>/', views.mark_as_delivered, name='mark_as_delivered'),

    # Отчети
    path('turnover-report/', views.turnover_report, name='turnover_report'),
    path('generate-turnover-report/', views.generate_turnover_report, name='generate_turnover_report'),
    path('earnings-report/', views.earnings_report, name='earnings_report'),
]
