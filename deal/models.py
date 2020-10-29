from django.contrib.auth.models import User
from django.db import models


class Deal(models.Model):
    """
    Модель сделки
    """
    customer = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='deals')
    item = models.CharField(verbose_name='Наименование товара', max_length=64)
    total = models.DecimalField(
        verbose_name='Сумма сделки', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='Колличество товара, шт')
    date = models.DateTimeField(verbose_name='Дата и время регистрации сделки')
