from django.contrib.auth import forms


class ShopUserCreationForm(forms.UserCreationForm):
    """
    Форма создания пользователя портала.
    """
    class Meta(forms.UserCreationForm.Meta):
        fields = forms.UserCreationForm.Meta.fields
