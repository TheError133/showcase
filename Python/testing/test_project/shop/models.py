from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import FloatField
from django.urls import reverse


class UserBalance(models.Model):
    """
    Модель баланса пользователя портала.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = FloatField(default=0.0)

    def __str__(self):
        return f'{self.user.username}: {self.balance}'

    def get_absolute_url(self):
        return reverse("balance-detail", kwargs={"pk": self.pk})
    

class Product(models.Model):
    """
    Модель товара магазина.
    """
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        if len(self.name) > 30:
            return f'{self.name[:30]}...'
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
