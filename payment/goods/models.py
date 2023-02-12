from django.db import models
from django.core import validators


class Item(models.Model):
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(validators=[
        validators.MinValueValidator(50),
        validators.MaxValueValidator(100000)
    ])


class Order(models.Model):
    items = models.ManyToManyField(Item,
                                   related_name='orders')
    customer_email = models.EmailField()
    amount = models.IntegerField()
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
