from django.urls import path
import django.contrib.auth.views as auth_views

from . import views


urlpatterns = [
    # Портал - скрипты.
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('detail/<pk>/', views.ScriptDetailView.as_view(), name='script_detail'),
    # Портал - пользователи.
    # Отключил доступ к странице создания пользователя.
    # Создавать пользователей пока может только админ.
    # path('user/create/', views.user_create, name='user-create'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password-change-done'),
    # API - отображение.
    path('api/list/', views.api_script_list, name='api-script-list'),
    path('api/list/<pk>/', views.api_script_detail, name='api-script-detail'),
    # API - добавление.
    path('api/script/add/', views.api_script_add, name='api-script-add'),
]
