from django import template

from ..models import Rating

register = template.Library()


@register.filter
def user_comment_exists(article, user):
    """
    Определение, есть ли в списке оценок оценка от конкретного пользователя.
    """
    return len(Rating.objects.filter(article=article, author=user)) > 0
