from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField


class Section(models.Model):
    """
    Модель раздела БЗ.
    """
    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Slug', max_length=100, unique=True)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    parent_section = models.ForeignKey(
        'self', verbose_name='Родительский раздел', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        if len(self.name) > 30:
            return f'{self.name[:30]}...'
        else:
            return self.name

    def get_absolute_url(self):
        return reverse('subsection-list', args=[self.slug])

    def get_section_articles(self):
        """
        Получение списка связанных с разделом статей.
        """
        return Article.objects.filter(section=self.id)

    def get_section_subsections(self):
        """
        Получение списка связанных с разделом подразделов.
        """
        return Section.objects.filter(parent_section=self.id)


class Article(models.Model):
    """
    Модель статьи БЗ.
    """
    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Slug', max_length=100, unique=True)
    text = RichTextField(verbose_name='Текст статьи')
    section = models.ForeignKey(Section, verbose_name='Родительский раздел', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        ordering = ['section', 'name']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        if len(self.name) > 30:
            return f'{self.name[:30]}...'
        else:
            return self.name

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.slug])

    def get_related_comments(self):
        """
        Получение списка связанных со статьей комментариев.
        """
        return Comment.objects.filter(article=self.id)

    def get_related_files(self):
        """
        Получение списка связанных со статьей файлов.
        """
        return File.objects.filter(article=self.id)

    def get_related_ratings(self):
        """
        Получение списка связанных со статьей оценок.
        """
        return Rating.objects.filter(article=self.id)


class File(models.Model):
    """
    Модель файлов статьи.
    """
    article = models.ForeignKey(Article, verbose_name='Связанная статья', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Файл', upload_to='files/%Y/%m/%d')
    added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['-added']

    def __str__(self):
        return f'{self.file.name} ({self.article})'

    def get_filename(self):
        return self.file.name.split('/')[-1]


class Comment(models.Model):
    """
    Модель комментариев к статье.
    """
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    def __str__(self):
        if len(self.text) > 30:
            return f'{self.text[:30]}...'
        else:
            return self.text


class Rating(models.Model):
    """
    Модель оценок по статье.
    """
    RATING_CHOICES = (
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Плохо'),
        (1, 'Очень плохо')
    )

    article = models.ForeignKey(Article, verbose_name='Связанная статья', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор оценки', on_delete=models.DO_NOTHING)
    value = models.IntegerField(verbose_name='Оценка', choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.author} - {self.value}'
