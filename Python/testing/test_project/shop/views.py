from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth import login

from .models import UserBalance, Product
from .forms import ShopUserCreationForm


class UserDetails(View):
    """
    Личный кабинет пользователя.
    """
    def get(self, request, *args, **kwargs):
        try:
            user_balance = get_object_or_404(UserBalance, pk=kwargs['pk'])
        except Http404:
            user_balance = UserBalance.objects.create(user=request.user, balance=0.0)
        context = {
            'user_balance': user_balance
        }

        return render(request, 'shop/user_detail.html', context)


class ProductListView(View):
    """
    Список товаров магазина.
    """
    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        context = {
            'product_list': product_list
        }

        return render(request, 'shop/product_list.html', context)


def user_create(request):
    """
    Создание пользователя портала.
    """
    if request.method == 'GET':
        return render(request, 'shop/user_create.html', {'form': ShopUserCreationForm})
    if request.method == 'POST':
        form = ShopUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:user-detail', user.id)
    else:
        form = ShopUserCreationForm()

    return render(request, 'shop/product_list.html', {'form': form})