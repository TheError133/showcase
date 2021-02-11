from django.urls import path
import django.contrib.auth.views as auth_views

from . import views


app_name = 'shop'
urlpatterns = [
    # Каталог магазина.
    path('products/', views.ProductListView.as_view(), name='product-list'),
    # Работа с пользователями.
    path('user/create/', views.user_create, name='user-create'),
    path('user/<pk>/', views.UserDetails.as_view(), name='user-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path(
        'password_change/', 
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), 
        name='password-change'),
    path(
        'password_change/done/', 
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password-change-done'),
]
