from django import template
from cart.models import Cart, CartItems

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_count(context):
    request = context['request']
    cart_count = 0
    if not request.user.is_anonymous:
        cart = Cart.objects.get(username=request.user)
        cart_items = CartItems.objects.filter(cart=cart)
        for item in cart_items:
            cart_count += item.quantity
    return cart_count