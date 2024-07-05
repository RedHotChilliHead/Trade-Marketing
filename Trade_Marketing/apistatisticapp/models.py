from django.db import models


class Event(models.Model):
    """
    Модель события
    """
    class Meta:
        ordering = ["date"]
    date = models.DateField(blank=False, null=False)  # date - дата события
    views = models.IntegerField(blank=True, null=True)  # views - количество показов
    clicks = models.IntegerField(blank=True, null=True)  # clicks - количество кликов
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # cost - стоимость кликов (в рублях с точностью до копеек)
