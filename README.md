# BettlePayment
### Description
Магазин с системой оплаты, реализованной на базе сервиса Stripe

### Tech
- Python 3.10
- Django 4.1.3
- Stripe

### Как запустить проект?
- Клонировать данный репозиторий
- установить виртуальное окружение и активировать его
- установить необходимые компоненты с помощью:
```pip install -r requirements.txt```
- В корневой папке(где находится settings.py) 'payment' создать файл '.env' и записать в него секретные ключи, к примеру:
```
   SECRET_KEY = awduaw123huhanj65o785lz
   STRIPE_PUBLISHABLE_KEY='pk_test_51MZcdQC09SxA8Y879Y2H19z1EcaxXmTQklnMY6UqjgRNrHTThc'
   STRIPE_SECRET_KEY='sk_test_51MZcdQC09SxA8Y87pUTjzCiDN9QqMYHrUbtHGyr4pYRJLvKk9wKjHX7xkW8u1HKzk381naIn7iA6800qeFPF7XT'
```
- Сделать миграции в БД с помощью:
```python manage.py migrate```
- После этих действий можно запустить сам django server:
```python manage.py runserver```
- Перейти на [localhost](http://127.0.0.1:8000/)

- Чтобы создать новый товары необходим доступ администратора:
```python manage.py createsuperuser```
- После создания товаров, его можно как добавлять в корзину, так и оплачивать сразу,
так же сделана реализация истории заказов для администратора

