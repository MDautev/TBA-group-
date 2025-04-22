"""
Конфигурация на Django Admin за приложението.

Този модул регистрира всички модели към Django Admin интерфейса,
позволявайки управление през административния панел.
"""

from django.contrib import admin
from .models import (
    User, Client, Employee, DeliveryPerson,
    Category, Restaurant, Product, Order, OrderItem, Delivery
)

# Регистрация на всички модели в admin панела
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(DeliveryPerson)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
