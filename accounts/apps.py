"""
Конфигурационен модул за Django приложението 'accounts'.

Този клас указва настройките на приложението и неговото име.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    AppConfig за приложението 'accounts'.

    Определя подразбиращото се primary key поле и името на приложението.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

