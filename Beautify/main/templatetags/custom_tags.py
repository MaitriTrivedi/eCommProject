from django import template
from products.models import CATEGORY_CHOICES
from account.models import Sellers

register = template.Library()

@register.simple_tag
def categories():
    return CATEGORY_CHOICES

@register.simple_tag(takes_context=True)
def is_seller(context):
    request = context['request']
    is_seller = False
    try :
        seller = Sellers.objects.get(user=request.user)
        if seller:
            is_seller = True
        else : is_seller = False
    except Exception as e:
        is_seller = False
   
    return is_seller