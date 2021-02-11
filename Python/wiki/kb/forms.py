from django.forms import ModelForm, TextInput

from .models import Section, Article, Comment, File, Rating


class SectionAddForm(ModelForm):
    """
    Форма добавления раздела.
    """
    class Meta:
        model = Section
        fields = ('name', 'slug')
        widgets = {
            'slug': TextInput(attrs={'placeholder': 'section-name-example'})
        }


class ArticleAddForm(ModelForm):
    """
    Форма добавления статьи.
    """
    class Meta:
        model = Article
        fields = ('name', 'slug', 'text')
        widgets = {
            'slug': TextInput(attrs={'placeholder': 'article-name-example'})
        }


class CommentAddForm(ModelForm):
    """
    Форма добавления комментария.
    """
    class Meta:
        model = Comment
        fields = ('text',)


class FileAddForm(ModelForm):
    """
    Форма добавления файла.
    """
    class Meta:
        model = File
        fields = ('file',)


class RatingAddForm(ModelForm):
    """
    Форма добавления оценки.
    """
    class Meta:
        model = Rating
        fields = ('value',)
