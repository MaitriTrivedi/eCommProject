from django.shortcuts import render
from django.urls import reverse
from cart.models import Cart, CartItems
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItems
from paypal.standard.forms import PayPalPaymentsForm
from main.models import Coupon
# Create your views here.
class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""
    
# pay :
@login_required
def pay(request):
    """
    Starts the payment process.
    """
    context={}
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('return_view')),   
        "cancel_return": request.build_absolute_uri(reverse('cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context["form"]= form   
    # return render(request, "payment.html", context)

    if request.method=='POST':
        current_user_cart=Cart.objects.get(username=request.user)
        user_cart_items=CartItems.objects.filter(cart=current_user_cart)
        order=Order.objects.create(username=request.user)
        order.save()
        for i in user_cart_items:
            temp=OrderItems.objects.create(order=order,products=i.products,quantity=i.quantity,total_price=i.total_price)
            temp.save()
        current_user_cart.delete()
        context['subtotal']=request.POST.get('subtotal')
        context['tax']=request.POST.get('tax')
        context['grandtotal']=request.POST.get('grandtotal')
        context['shipping']=request.POST.get('shipping')
    # valid_ipn_received.connect(show_me_the_money)
    return render(request,'payment/pay.html',context)


    

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

# def show_me_the_money(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # WARNING !
#         # Check that the receiver email is the same we previously
#         # set on the `business` field. (The user could tamper with
#         # that fields on the payment form before it goes to PayPal)
#         if ipn_obj.receiver_email != "receiver_email@example.com":
#             # Not a valid payment
#             return

#         # ALSO: for the same reason, you need to check the amount
#         # received, `custom` etc. are all what you expect or what
#         # is allowed.

#         # Undertake some action depending upon `ipn_obj`.
#         if ipn_obj.custom == "premium_plan":
#             price = ...
#         else:
#             price = ...

#         if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
#             ...
#     else:
#         #...


def return_view(request):
    return render(request,'payment/return.html')

def cancel_view(request):
    return render(request,'payment/cancel.html')

# checkout :
@login_required
def checkout(request):
    """
    Takes the user to the payment page.
    """
    context = {}
    if request.method=='POST':
        context['subtotal']=request.POST.get('subtotal')
        context['tax']=request.POST.get('tax')
        context['grandtotal']=request.POST.get('grandtotal')
        context['shipping']=request.POST.get('shipping')
        if request.POST.get('coupon'):
            context['couponcode']=request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(couponcode=context['couponcode']).first()
            if coupon_obj!=None:
                discount_price= coupon_obj.discount
                if int(float( context['grandtotal'] )) > ( coupon_obj.min_amount ) and coupon_obj.is_expired==False:
                    context['grandtotal']=int(float(context['grandtotal']))-discount_price
    return render(request,'payment/checkout.html',context)

