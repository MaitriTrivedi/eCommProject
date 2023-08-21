import math

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View   

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from account.models import UserData
from .models import Cart, CartItems
from products.models import Products
from django.shortcuts import redirect
from django.urls import reverse
# from main.views import session

# session = {'username':'','products':Products.objects.all()}


# CART :
# Add product to cart :
@login_required
def addToCart(request,product_id):
    """
    Adds product to user's cart.
    """
    product = Products.objects.get(product_id=product_id)
    user = request.user
    cart , _ = Cart.objects.get_or_create(username=user,is_paid=False)
    cart.save()
    if CartItems.objects.filter(cart=cart,products=product):
        temp=CartItems.objects.filter(cart=cart,products=product).first()
        temp.quantity = temp.quantity + 1
        product.quantity=product.quantity-1
        product.save()
        temp.total_price= temp.quantity * product.price
        temp.save()
    else:
        cart_items = CartItems.objects.create(cart=cart,products=product)
        cart_items.quantity = 1
        product.quantity=product.quantity-1
        product.save()
        cart_items.total_price= cart_items.quantity * product.price
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Update cart :
@login_required
def updatecart(request):
    """
    Increase , decrease quantity of a particular product and removes a particular product.
    """
    sign = request.POST.get('sign')
    id=request.POST.get('id')
    remove = request.POST.get('remove')
    context = {'cart':Cart.objects.filter(is_paid=False,username=request.user),'products':[],'cart_items':[],'length':0,'items':'','price':[],'subtotal':0}
    try :
        cart_items = CartItems.objects.filter(cart=context['cart'][0])
    except IndexError:
        messages.error(request,'No Items in Cart')
        return render(request,'main/cart.html',context)
    subtotal=0
    temp = Products.objects.get(product_id=id)

    # to remove
    if remove=='remove':
        objects_delete=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp)
        temp.quantity=temp.quantity+objects_delete[0].quantity
        temp.save()
        objects_delete.delete()
        return HttpResponseRedirect('cart',context)
    
    # to decrease the quantity
    if sign=='-':
        try :
            cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
            cart_objects.quantity=cart_objects.quantity-1
        except CartItems.DoesNotExist:
            pass
        temp.quantity=temp.quantity+1
        temp.save()
        cart_objects.total_price=cart_objects.total_price-(cart_objects.products.price)
        if cart_objects.quantity==0:
            cart_objects.delete()
        else:
            cart_objects.save()

    # to increase the quantity
    if sign=='+':
        try :
            cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
            if cart_objects:
                cart_objects.quantity=cart_objects.quantity+1
        except CartItems.DoesNotExist:
            cart_objects.quantity = 1
        
        temp.quantity=temp.quantity-1
        temp.save()
        cart_objects.total_price=cart_objects.total_price+(cart_objects.products.price)
        cart_objects.save()

    # context = {
    #     'previous_url': request.META.get('HTTP_REFERER')
    # }
    # return render(request, 'main/cart.html', context)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# View cart items :
@login_required
def cart(request):
    """
    Shows user the items in the cart.
    """
    sign = request.POST.get('sign')
    id=request.POST.get('id')
    remove = request.POST.get('remove')
    context = {'cart':[],'cart_items':[]}
    context['cart']=Cart.objects.filter(is_paid=False,username=request.user).first()
    try :
        context['cart_items']=CartItems.objects.filter(cart=context['cart'])
    except IndexError:
        messages.error(request,'No Items in Cart')
        return render(request,'main/order.html',context)
    totalQuantity=0
    totalCost=0
    for i in range(len(context['cart_items'])):
        totalCost=totalCost+(context['cart_items'][i].quantity*context['cart_items'][i].products.price)
        totalQuantity=totalQuantity+(context['cart_items'][i].quantity)
    context['subtotal']=totalCost
    context['tax']=totalCost*(0.18)
    context['grandtotal']=totalCost+100+context['tax']
    return render(request,'main/cart.html',context)