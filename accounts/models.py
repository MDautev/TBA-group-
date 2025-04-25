from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Разширен потребителски модел, базиран на Django AbstractUser.

    Добавя ролеви флагове за идентификация на типа потребител:
    клиент, служител или доставчик.
    
    Attributes:
        is_client (bool): Дали потребителят е клиент.
        is_employee (bool): Дали потребителят е служител.
        is_delivery_person (bool): Дали потребителят е доставчик.
    """
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_delivery_person = models.BooleanField(default=False)


class Client(models.Model):
    """
    Модел, представящ клиент.

    Свързан е едно-към-едно с User и съдържа адрес за доставка.

    Attributes:
        user (User): Потребителският акаунт, свързан с клиента.
        address (str): Адресът на клиента.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=255)


class Employee(models.Model):
    """
    Модел за служител.

    Съдържа информация за отдела, в който работи служителят.

    Attributes:
        user (User): Свързаният потребител.
        department (str): Име на отдела.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=100)


class DeliveryPerson(models.Model):
    """
    Модел за доставчик.

    Съдържа тип на превозното средство.

    Attributes:
        user (User): Свързаният потребител.
        vehicle_type (str): Типът на превозното средство.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vehicle_type = models.CharField(max_length=50)


class Category(models.Model):
    """
    Категория продукти (напр. "Пици", "Напитки").

    Attributes:
        name (str): Името на категорията.
        description (str): Допълнително описание (по избор).
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """
    Модел за ресторант, който предлага продукти.

    Attributes:
        name (str): Името на ресторанта.
        address (str): Адресът на ресторанта.
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('pizza', 'Пица'),
        ('pasta', 'Паста'),
        ('salad', 'Салата'),
        ('dessert', 'Десерт'),
        ('drink', 'Напитка'),
    ]


    """
    Продукт, предлаган от ресторант (напр. пица, напитка).

    Attributes:
        restaurant (Restaurant): Ресторантът, който предлага продукта.
        name (str): Името на продукта.
        description (str): Описание на продукта (по избор).
        price (Decimal): Цена на продукта.
    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Без дефолтна стойност

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Order(models.Model):
    """
    Поръчка, направена от клиент, съдържаща продукти.

    Attributes:
        client (Client): Клиентът, който е направил поръчката.
        products (ManyToMany[Product]): Продуктите в поръчката.
        total_price (Decimal): Обща цена на поръчката.
        status (str): Статус на поръчката.
        created_at (datetime): Дата и час на създаване.
    """
    STATUS_CHOICES = [
        ('pending', 'В процес'),
        ('shipped', 'Изпратена'),
        ('delivered', 'Доставена'),
        ('cancelled', 'Отказана'),
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField('Product', through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    delivery_person = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='deliveries')
    address = models.CharField(max_length=255, blank=True, null=True)  # Поле за адрес
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Поле за телефонен номер

    def __str__(self):
        return f"Поръчка #{self.id} от {self.client.user.username}"


class OrderItem(models.Model):
    """
    Единичен продукт в поръчка.

    Свързва продукт и поръчка с количество и цена.

    Attributes:
        order (Order): Поръчката, към която принадлежи.
        product (Product): Продуктът, който е поръчан.
        quantity (int): Брой на продукта.
        price (Decimal): Цена на продукта за дадената поръчка.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Delivery(models.Model):
    """
    Доставка, асоциирана с поръчка.

    Съдържа информация за доставчика, адрес и време на доставка.

    Attributes:
        order (Order): Свързаната поръчка.
        delivery_person (User): Потребителят-доставчик.
        delivery_address (str): Адрес за доставка.
        delivery_time (datetime): Час на доставка (по избор).
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_person = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_delivery_person': True})
    delivery_address = models.CharField(max_length=255)
    delivery_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Доставка за поръчка #{self.order.id}"


class CartItem(models.Model):
    """
    Модел за артикул в количката за пазаруване.

    Този модел съхранява информация за:
    - Кой потребител е добавил артикула
    - Кой продукт е добавен
    - Количество на продукта

    Атрибути:
        user (ForeignKey): Връзка към потребителя, който е добавил артикула.
                         При изтриване на потребителя, артикулите се изтриват автоматично (CASCADE).
                         
        product (ForeignKey): Връзка към продукта в количката.
                            При изтриване на продукта, артикулите се изтриват автоматично (CASCADE).
                            
        quantity (PositiveIntegerField): Количество на продукта. Минимална стойност 1 (по подразбиране).

    Методи:
        __str__: Представяне на обекта като низ във формат:
                "{количество} x {име на продукт} (Потребител: {потребителско име})"

    Пример:
        >>> item = CartItem.objects.first()
        >>> print(item)
        "2 x Пица (Потребител: ivan_georgiev)"

    Връзки:
        - Свързан с User модела чрез ForeignKey
        - Свързан с Product модела чрез ForeignKey

    Важно:
        - Количеството винаги трябва да е положително число
        - Всеки артикул в количката е уникална комбинация от потребител и продукт
        - Препоръчително е да се използва заедно с Cart модел за управление на колички
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Потребител: {self.user.username})"
