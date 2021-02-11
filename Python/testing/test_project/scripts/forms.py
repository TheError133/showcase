from django.contrib.auth import forms
from django import forms as user_forms


class ScriptUserCreationForm(forms.UserCreationForm):
    """
    Форма создания пользователя портала.
    """
    class Meta(forms.UserCreationForm.Meta):
        fields = forms.UserCreationForm.Meta.fields
