from django import template
from products.models import CATEGORY_CHOICES

register = template.Library()

@register.simple_tag
def categories():
    return CATEGORY_CHOICES