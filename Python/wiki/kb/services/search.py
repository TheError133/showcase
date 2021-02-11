from django.contrib.postgres.search import TrigramSimilarity

from kb.models import Article, Section


def get_articles(search_string):
    """
    Получение списка статей по строке поиска.
    """
    articles = (
        Article.objects.annotate(
            similarity_name=TrigramSimilarity('name__unaccent', search_string),
        ).filter(similarity_name__gte=0.3) |
        Article.objects.annotate(
            similarity_text=TrigramSimilarity('text__unaccent', search_string),
        ).filter(similarity_text__gte=0.3)
    ).distinct()

    return articles


def get_sections(search_string):
    """
    Получение списка разделов по строке поиска.
    """
    return Section.objects.annotate(
        similarity=TrigramSimilarity('name__unaccent', search_string),
    ).filter(similarity__gte=0.3).distinct()
