from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import View, CreateView, UpdateView, DeleteView

from .models import Section, Article, Comment, File, Rating
from .forms import SectionAddForm, ArticleAddForm, CommentAddForm, FileAddForm, RatingAddForm
from .services.search import get_articles, get_sections


class UserCreationView(CreateView):
    """
    Создание пользователя.
    """
    form_class = UserCreationForm
    template_name = 'kb/user_create.html'
    success_url = reverse_lazy('section-list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)

        return result


class SectionView(View):
    """
    Корневой список разделов и статей БЗ.
    """
    def get(self, request, *args, **kwargs):
        sections = Section.objects.filter(parent_section=None)

        return render(request, 'kb/section_list.html', {'sections': sections})

    def post(self, request, *args, **kwargs):
        if 'search_string' in request.POST:
            # POST-запрос для поиска по порталу.
            search_string = request.POST.get('search_string')
            articles = get_articles(search_string)
            sections = get_sections(search_string)
            context = {
                'articles': articles,
                'sections': sections,
                'search_string': search_string
            }

            return render(request, 'kb/search_results.html', context)


class SectionAddView(CreateView):
    """
    Создание раздела БЗ.
    """
    template_name = 'kb/section_add.html'
    form_class = SectionAddForm

    def get_success_url(self, slug=None):
        return reverse('subsection-list', args=[slug])

    def form_valid(self, form):
        user = self.request.user
        section = form.save(commit=False)
        section.author = user
        section.parent_section = None
        section.save()

        return HttpResponseRedirect(self.get_success_url(section.slug))


class SubsectionView(View):
    """
    Список разделов и статей подраздела.
    """
    def get(self, request, *args, **kwargs):
        section = get_object_or_404(Section, slug=kwargs['slug'])
        subsections = section.get_section_subsections()
        articles = section.get_section_articles()
        context = {
            'section': section,
            'subsections': subsections,
            'articles': articles
        }

        return render(request, 'kb/subsection_list.html', context)

    def post(self, request, *args, **kwargs):
        if 'search_string' in request.POST:
            # POST-запрос для поиска по порталу.
            search_string = request.POST.get('search_string')
            articles = get_articles(search_string)
            sections = get_sections(search_string)
            context = {
                'articles': articles,
                'sections': sections,
                'search_string': search_string
            }

            return render(request, 'kb/search_results.html', context)


class SubsectionAddView(CreateView):
    """
    Создание подраздела БЗ.
    """
    template_name = 'kb/subsection_add.html'
    form_class = SectionAddForm

    def get_success_url(self):
        subsection_slug = self.kwargs.get('slug')
        return reverse('subsection-list', args=[subsection_slug])

    def form_valid(self, form):
        user = self.request.user
        section = form.save(commit=False)
        section.author = user
        section.parent_section = get_object_or_404(Section, slug=self.kwargs.get('slug'))
        section.save()

        return HttpResponseRedirect(self.get_success_url())


class SubsectionEditView(UpdateView):
    """
    Обновление информации по разделу.
    """
    model = Section
    template_name = 'kb/subsection_edit.html'
    fields = ('name', 'slug', 'parent_section')

    def get_success_url(self):
        subsection_slug = self.kwargs.get('slug')
        return reverse('subsection-list', args=[subsection_slug])


class SubsectionDeleteView(DeleteView):
    """
    Удаление раздела.
    """
    model = Section
    template_name = 'kb/subsection_delete.html'
    success_url = reverse_lazy('section-list')


class ArticleDetailView(View):
    """
    Информация по статье.
    """
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=kwargs['slug'])
        comments = article.get_related_comments()
        files = article.get_related_files()
        ratings = article.get_related_ratings()
        context = {
            'article': article,
            'comments': comments,
            'files': files,
            'ratings': ratings
        }

        return render(request, 'kb/article_detail.html', context)

    def post(self, request, *args, **kwargs):
        if 'search_string' in request.POST:
            # POST-запрос для поиска по порталу.
            search_string = request.POST.get('search_string')
            articles = get_articles(search_string)
            sections = get_sections(search_string)
            context = {
                'articles': articles,
                'sections': sections,
                'search_string': search_string
            }

            return render(request, 'kb/search_results.html', context)
        elif 'comment_string' in request.POST:
            # POST-запрос для добавления комментария.
            comment_text = request.POST.get('comment_string')
            article = get_object_or_404(Article, slug=kwargs['slug'])
            user = request.user
            comment = Comment(article=article, author=user, text=comment_text)
            comment.save()

            return HttpResponseRedirect(article.get_absolute_url())


class ArticleAddView(CreateView):
    """
    Создание статьи БЗ.
    """
    form_class = ArticleAddForm
    template_name = 'kb/article_add.html'

    def get_success_url(self, slug=None):
        return reverse('article-detail', args=[slug])

    def form_valid(self, form):
        user = self.request.user
        article = form.save(commit=False)
        article.author = user
        article.section = get_object_or_404(Section, slug=self.kwargs.get('slug'))
        article.save()

        return HttpResponseRedirect(self.get_success_url(article.slug))


class ArticleUpdateView(UpdateView):
    """
    Обновление информации по статье.
    """
    model = Article
    fields = ('name', 'slug', 'text', 'section')
    template_name = 'kb/article_edit.html'


class ArticleDeleteView(DeleteView):
    """
    Удаление статьи.
    """
    model = Article
    template_name = 'kb/article_delete.html'

    def get_success_url(self):
        subsection_slug = self.object.section.slug
        return reverse('subsection-list', args=[subsection_slug])


def main_page_redirect(request):
    """
    Перенаправление на страницу со статьями.
    """
    return redirect('section-list')


class CommentAddView(CreateView):
    """
    Добавление комментария.
    """
    form_class = CommentAddForm
    template_name = 'kb/comment_add.html'

    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        return reverse('article-detail', args=[article_slug])

    def form_valid(self, form):
        user = self.request.user
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        comment = form.save(commit=False)
        comment.author = user
        comment.article = article
        comment.save()

        return HttpResponseRedirect(self.get_success_url())


class CommentEditView(UpdateView):
    """
    Редактирование комментариев.
    """
    model = Comment
    fields = ('text',)
    template_name = 'kb/comment_edit.html'

    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        return reverse('article-detail', args=[article_slug])


class CommentDeleteView(DeleteView):
    """
    Удаление комментария.
    """
    model = Comment
    template_name = 'kb/comment_delete.html'

    def get_success_url(self):
        article_slug = self.object.article.slug
        return reverse('article-detail', args=[article_slug])


class FileAddView(CreateView):
    """
    Добавление файла.
    """
    form_class = FileAddForm
    template_name = 'kb/file_add.html'

    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        return reverse('article-detail', args=[article_slug])

    def form_valid(self, form):
        user = self.request.user
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        file = form.save(commit=False)
        file.author = user
        file.article = article
        file.save()

        return HttpResponseRedirect(self.get_success_url())


class FileDeleteView(DeleteView):
    """
    Удаление файла.
    """
    model = File
    template_name = 'kb/file_delete.html'

    def get_success_url(self):
        article_slug = self.object.article.slug
        return reverse('article-detail', args=[article_slug])


class RatingAddView(CreateView):
    """
    Добавление оценки для статьи.
    """
    form_class = RatingAddForm
    template_name = 'kb/rating_add.html'

    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        return reverse('article-detail', args=[article_slug])

    def form_valid(self, form):
        user = self.request.user
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        file = form.save(commit=False)
        file.author = user
        file.article = article
        file.save()

        return HttpResponseRedirect(self.get_success_url())


class RatingEditView(UpdateView):
    """
    Изменение оценки по статье.
    """
    model = Rating
    fields = ('value',)
    template_name = 'kb/rating_edit.html'

    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        return reverse('article-detail', args=[article_slug])


class RatingDeleteView(DeleteView):
    """
    Удаление оценки статьи.
    """
    model = Rating
    template_name = 'kb/rating_delete.html'

    def get_success_url(self):
        article_slug = self.object.article.slug
        return reverse('article-detail', args=[article_slug])
