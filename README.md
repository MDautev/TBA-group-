````markdown
# 🍔 TBA Food Delivery Platform
````
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Модерна платформа за хранителни доставки, обединяваща клиенти, ресторанти и куриери в едно унифицирано решение.

## 📖 Съдържание

- [🔩 Конфигурация](#-конфигурация)
- [🔧 Инсталация](#-инсталация)
- [📁 Структура на проекта](#-структура-на-проекта)
- [📚 Документация](#-документация)
- [⚙️ Функционалности](#%EF%B8%8F-функционалности)
- [📈 Бизнес модел](#-бизнес-модел)
- [👨‍💻 Екип](#-екип)

 ## 🔩 Конфигурация

1. **Създайте `.env` файл:**

```bash
cp .env.example .env
```

2. **Редактирайте настройките в `settings.py`:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'food_delivery',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔧 Инсталация

1. **Клонирайте хранилището:**

```bash
git clone https://github.com/MDautev/TBA-group.git
cd TBA-group
```

2. **Създайте и активирайте виртуална среда:**

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. **Инсталирайте зависимостите:**

```bash
pip install -r requirements.txt
```

4. **Конфигурирайте базата данни в `FOOD_DELIVERY_WEB/settings.py`**

5. **Изпълнете миграциите:**

```bash
python manage.py migrate
```

6. **Стартирайте сървъра:**

```bash
python manage.py runserver
```

## 📁 Структура на проекта

```
TBA-group/
├── FOOD_DELIVERY_WEB/         # Основният Django проект
│   ├── settings.py            # Настройки и конфигурация
│   ├── urls.py                # URL маршрутизация
│   └── ...
├── manage.py                  # Django CLI
├── requirements.txt           # Python зависимости
├── .gitignore
├── Lean_Canvas_TBA_Group.pdf # Бизнес план
└── README.md                  # Документация
```

## 📚 Документация

📝 **Пълната техническа документация на кода** е реализирана чрез **docstring-ове** директно в сорс файловете (Python модули и класове).

Препоръчва се използването на инструменти като `pydoc`, `Sphinx` или IDE (напр. VS Code, PyCharm), за да се визуализират коментарите по по-структуриран начин.

---

## ⚙️ Функционалности

### 🔑 Основни

- Управление на потребители: клиенти, ресторанти, куриери
- Обработка и проследяване на поръчки в реално време
- Аналитичен панел за ресторанти с ключови метрики
- Респонсивен интерфейс за всички роли в системата

### 🛠 Технологии

- **Backend:** Django 5.2
- **База данни:** PostgreSQL
- **REST API:** Django REST Framework _(в процес на разработка)_


## 📈 Бизнес модел

Платформата е изградена около устойчив и мащабируем бизнес модел, базиран на Lean Canvas.

### 📊 Основни метрики

- Брой поръчки (дневни/седмични)
- Средно време за доставка
- Ниво на удовлетвореност и изпълнение на поръчки

### 💰 Приходни потоци

- Комисионни от всяка поръчка
- Абонаменти за ресторанти
- Такси за доставка

📄 Виж [Lean Canvas документа](./Lean_Canvas_TBA_Group.pdf)

## 👨‍💻 Екип

Проектът се разработва от студенти, обединени около идеята за дигитална трансформация в доставките на храна.

🔗 Виж всички участници: [GitHub Contributors](https://github.com/MDautev/TBA-group-/graphs/contributors)

