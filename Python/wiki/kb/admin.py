from django.contrib import admin

from . import models


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_section', 'author')
    list_filter = ('created',)
    fields = ('name', 'slug', ('parent_section', 'author'))
    prepopulated_fields = {'slug': ('name',)}


class FileInlines(admin.TabularInline):
    model = models.File
    max_num = 2


class CommentInline(admin.TabularInline):
    model = models.Comment
    max_num = 2


class RatingInline(admin.TabularInline):
    model = models.Rating
    max_num = 2


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'author')
    list_filter = ('created',)
    fields = ('name', 'slug', ('section', 'author'), 'text')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        FileInlines,
        CommentInline,
        RatingInline
    ]

