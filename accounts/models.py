from decimal import Decimal

from django.core.mail import send_mail
from django.db import models, transaction
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
    def __str__(self):
        return self.user.username


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
    total_turnover = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Общ оборот, генериран от доставчика"
    )
    total_bonuses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Общо получени бонуси"
    )


    def __str__(self):
        return self.user.username


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
    Полета:
        client (ForeignKey): Свързана клиентска поръчка.
        products (ManyToManyField): Продукти, свързани с поръчката чрез `OrderItem`.
        total_price (DecimalField): Обща стойност на поръчката.
        status (CharField): Статус на поръчката (например, 'В процес', 'Изпратена').
        created_at (DateTimeField): Дата и час на създаване на поръчката.
        delivery_person (ForeignKey): Доставчик, който се свързва с поръчката.
        address (CharField): Адрес за доставка.
        phone_number (CharField): Телефонен номер на клиента.

    Методи:
        save: Записва поръчката в базата данни и при необходимост обработва бонусите за доставчика.
        _check_and_apply_bonus: Приложение на бонуси към доставчика при изпълнение на условията.
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
    delivery_person = models.ForeignKey(
        'DeliveryPerson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    address = models.CharField(max_length=255, blank=True, null=True)  # Поле за адрес
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Поле за телефонен номер

    def save(self, *args, **kwargs):
        """
        Записва поръчката и при промяна на статуса на 'delivered' проверява и прилага бонуси за доставчика.

        Ако поръчката е нова или статусът е променен на 'delivered', методът проверява дали доставчикът 
        има право на бонуси на база стойността на поръчката и общия му оборот.

        Аргументи:
            *args: Допълнителни аргументи за метода.
            **kwargs: Допълнителни ключови аргументи за метода.
        """
        is_new = self._state.adding

        # Ако поръчката вече съществува, взимаме стария статус
        if not is_new:
            old_order = Order.objects.get(pk=self.pk)
            old_status = old_order.status
        else:
            old_status = None

        # Първо записваме без да тригерираме бонус логиката
        super().save(*args, **kwargs)

        # Проверка за бонус (само при промяна на статус на 'delivered')
        if (is_new or old_status != 'delivered') and self.status == 'delivered':
            if not hasattr(self, '_bonus_processed'):  # Критична проверка!
                with transaction.atomic():
                    delivery_person = DeliveryPerson.objects.select_for_update().get(pk=self.delivery_person_id)
                    self._check_and_apply_bonus(delivery_person)  # Подаваме delivery_person
                    self._bonus_processed = True

    def _check_and_apply_bonus(self, delivery_person):
        """
        Проверява дали доставчикът има право на бонус и го прилага, ако е необходимо.

        Прилага бонус, ако доставчикът е достигнал минималния оборот, 
        зададен в настройките на бонусите.

        Аргументи:
            delivery_person (DeliveryPerson): Доставчикът, за когото ще се провери и приложи бонус.
        """
        bonus_settings = BonusSettings.objects.filter(is_active=True).first()

        # Добавяме САМО стойността на поръчката (без бонуса)
        delivery_person.total_turnover += Decimal(str(self.total_price))

        # Проверка за бонус
        if bonus_settings and delivery_person.total_turnover >= bonus_settings.min_turnover:
            delivery_person.total_turnover += bonus_settings.bonus_amount
            delivery_person.total_bonuses += bonus_settings.bonus_amount

        delivery_person.save(update_fields=['total_turnover', 'total_bonuses'])

    def __str__(self):
        """
        Връща текстово представяне на поръчката, включващо нейния ID и потребителското име на клиента.

        Връща:
            str: Текстово представяне на поръчката.
        """
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


class BonusSettings(models.Model):
    """
    Модел, който съхранява настройките за бонуси на доставчици.

    Полета:
        min_turnover (DecimalField): Минималният оборот, който доставчикът трябва да постигне, за да получи бонус.
        bonus_amount (DecimalField): Сумата на бонуса, която се дава на доставчика, ако минималният оборот е достигнат.
        is_active (BooleanField): Флаг, който показва дали настройката е активна или не.

    Методи:
        __str__: Връща текстово представяне на бонус настройката.
    """
    
    min_turnover = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Минимален оборот за бонус"
    )
    bonus_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сума на бонуса"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна настройка"
    )

    class Meta:
        verbose_name = "Бонус настройка"
        verbose_name_plural = "Бонус настройки"

    def __str__(self):
        """
        Връща текстово представяне на бонус настройката.

        Връща:
            str: Текстовото представяне, включващо сумата на бонуса и минималния оборот.
        """
        return f"Бонус: {self.bonus_amount} лв. при оборот ≥ {self.min_turnover} лв."
