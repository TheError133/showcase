from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserScript(models.Model):
    """
    Модель скрипта пользователя.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    script = models.TextField()

    def __str__(self):
        return f'{self.author}: {self.name}'

    def get_absolute_url(self):
        return reverse('script_detail', kwargs={'pk': self.pk})
    
