from django.contrib import admin

from .models import UserScript

@admin.register(UserScript)
class UserScriptAdmin(admin.ModelAdmin):
    pass
