from django.contrib import admin

from .models import UserBalance, Product


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
