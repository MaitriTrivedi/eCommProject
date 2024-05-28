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
from django.http import JsonResponse
# from main.views import session

# session = {'username':'','products':Products.objects.all()}


# CART :
# Add product to cart :
@login_required
def addToCart(request,product_id):
    """
    Adds product to user's cart.
    """
    # import pdb;pdb.set_trace()
    product = Products.objects.get(product_id=product_id)
    user = request.user
    cart , _ = Cart.objects.get_or_create(username=user,is_paid=False)
    cart.save()
    if CartItems.objects.filter(cart=cart,products=product):
        temp=CartItems.objects.filter(cart=cart,products=product).first()
        temp.quantity = temp.quantity + 1
        temp.total_price= temp.quantity * temp.products.price
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
def update_cart(request):
    if request.method == "POST" :#and request.is_ajax():
        # Get the data from the AJAX request
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        cart = Cart.objects.get(username=request.user)
        product = Products.objects.get(product_id=product_id)
        cart_item = CartItems.objects.get(cart=cart,products=product)
        
        data = {}
        # product = get_object_or_404(Products, id=product_id)
        if action == "+":
            cart_item.quantity += 1
            cart_item.total_price=cart_item.quantity * cart_item.products.price
            product.quantity -= 1
            product.save()
            cart_item.save()
            data["quantity"]=cart_item.quantity
            data["subtotal"]=cart_item.quantity * cart_item.products.price
        elif action == "remove":
            product.quantity -= cart_item.quantity
            product.save()
            cart_item.delete()
            data["quantity"]=0
            data["subtotal"]=0
        elif action == "-":
            cart_item.quantity -= 1
            product.quantity += 1
            product.save()
            if cart_item.quantity == 0:
                cart_item.delete()
                data["quantity"]=0
                data["subtotal"]=0
            else :
                cart_item.total_price=cart_item.quantity * cart_item.products.price
                cart_item.save()
                data["quantity"]=cart_item.quantity
                data["subtotal"]=cart_item.quantity * cart_item.products.price
        data["cart_quantity"] = CartItems.objects.filter(cart=cart).count()
        
        return JsonResponse(data)
    
    # Handle other HTTP methods or non-AJAX requests here
    return HttpResponseBadRequest("Bad Request")


# def updatecart(request):
#     """
#     Increase , decrease quantity of a particular product and removes a particular product.
#     """
#     sign = request.POST.get('sign')
#     id=request.POST.get('id')
#     remove = request.POST.get('remove')
#     context = {'cart':Cart.objects.filter(is_paid=False,username=request.user),'products':[],'cart_items':[],'length':0,'items':'','price':[],'subtotal':0}
#     try :
#         cart_items = CartItems.objects.filter(cart=context['cart'][0])
#     except IndexError:
#         messages.error(request,'No Items in Cart')
#         # return render(request,'cart/cart.html',context)
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         return redirect("/cart/mycart/")
    
#     subtotal=0
#     temp = Products.objects.get(product_id=id)
#     print("-------------------------------------")
#     print(remove)
#     print("-------------------------------------")
#     # to remove
#     if remove=='remove':
#         objects_delete=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp)
#         print(objects_delete)
#         temp.quantity=temp.quantity+objects_delete[0].quantity
#         temp.save()
#         objects_delete.delete()
#         # return HttpResponseRedirect('cart',context)
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         return redirect("/cart/mycart/")
    
#     # to decrease the quantity
#     if sign=='-':
#         try :
#             cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
#             cart_objects.quantity=cart_objects.quantity-1
#         except ObjectDoesNotExist:
#             pass
#         temp.quantity=temp.quantity+1
#         temp.save()
#         cart_objects.total_price=cart_objects.total_price-(cart_objects.products.price)
#         if cart_objects.quantity==0:
#             cart_objects.delete()
#         else:
#             cart_objects.save()

#     # to increase the quantity
#     if sign=='+':
#         try :
#             cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
#             if cart_objects:
#                 cart_objects.quantity=cart_objects.quantity+1
#         except ObjectDoesNotExist:
#             cart_objects.quantity = 1
        
#         temp.quantity=temp.quantity-1
#         temp.save()
#         if cart_objects:
#             cart_objects.total_price=cart_objects.total_price+(cart_objects.products.price)
#             cart_objects.save()
#         else :
#             cart_obj = CartItems.objects.create(cart=context["cart"][0],products=temp,total_price=temp.price)
#             cart_obj.save()
       

#     # context = {
#     #     'previous_url': request.META.get('HTTP_REFERER')
#     # }
#     # return render(request, 'cart/cart.html', context)
#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     # return HttpResponseRedirect('cart',context)
#     return redirect("/cart/mycart/")

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
        return render(request,'orders/order.html',context)
    totalQuantity=0
    totalCost=0
    for i in range(len(context['cart_items'])):
        totalCost=totalCost+(context['cart_items'][i].quantity*context['cart_items'][i].products.price)
        totalQuantity=totalQuantity+(context['cart_items'][i].quantity)
    context['subtotal']=totalCost
    context['tax']=totalCost*(0.18)
    context['grandtotal']=totalCost+100+context['tax']
    context['cart_item_quantity'] = len(context["cart_items"])
    return render(request,'cart/cart.html',context)
