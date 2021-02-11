from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    # Пользователи.
    path('user/create/', views.UserCreationView.as_view(), name='user-create'),
    path('user/login/', auth_views.LoginView.as_view(), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/password_change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    # В name подчеркивания, поскольку это шаблонное название вьюшки.
    path('user/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Разделы.
    path('sections/', views.SectionView.as_view(), name='section-list'),
    path('sections/list/<slug:slug>/', views.SubsectionView.as_view(), name='subsection-list'),
    path('sections/add/section/', views.SectionAddView.as_view(), name='section-add'),
    path('sections/add/subsection/<slug:slug>/', views.SubsectionAddView.as_view(), name='subsection-add'),
    path('sections/edit/subsection/<slug>/', views.SubsectionEditView.as_view(), name='subsection-edit'),
    path('sections/delete/subsection/<slug>/', views.SubsectionDeleteView.as_view(), name='subsection-delete'),
    # Статьи.
    path('article/detail/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('sections/add/article/<slug:slug>/', views.ArticleAddView.as_view(), name='article-add'),
    path('article/edit/<slug:slug>/', views.ArticleUpdateView.as_view(), name='article-edit'),
    path('article/delete/<slug>/', views.ArticleDeleteView.as_view(), name='article-delete'),
    # Статьи - комментарии.
    path('article/add/comment/<slug:slug>/', views.CommentAddView.as_view(), name='article-comment-add'),
    path('article/edit/comment/<slug>/<pk>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('article/delete/comment/<pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    # Статьи - файлы.
    path('article/add/file/<slug:slug>/', views.FileAddView.as_view(), name='article-file-add'),
    path('article/delete/file/<pk>/', views.FileDeleteView.as_view(), name='file-delete'),
    # Статьи - оценки.
    path('article/add/rating/<slug:slug>/', views.RatingAddView.as_view(), name='article-rating-add'),
    path('article/edit/rating/<slug>/<pk>/', views.RatingEditView.as_view(), name='rating-edit'),
    path('article/delete/rating/<pk>/', views.RatingDeleteView.as_view(), name='rating-delete'),
    # Поиск.
    path('search/', TemplateView.as_view(), name='search-results'),
    # Перенаправление на главную страницу всех некорректных адресов.
    path('', views.main_page_redirect)
]
