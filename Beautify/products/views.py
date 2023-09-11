from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Products, Wishlist, WishlistItems
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def addtowishlist(request,product_id):
    """
    Adds product to user's cart.
    """
    # import pdb;pdb.set_trace()
    product = Products.objects.get(product_id=product_id)
    user = request.user
    cart , _ = Wishlist.objects.get_or_create(username=user)
    cart.save()
    if WishlistItems.objects.filter(wishlist=cart,products=product):
        messages.error(request,'Item already in Wishlist')
        return redirect("/products/wishlist/")
    else:
        cart_items = WishlistItems.objects.create(wishlist=cart,products=product)
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Update cart :
@login_required
# def updatewishlist(request):
#     """
#     Increase , decrease quantity of a particular product and removes a particular product.
#     """
#     id = request.POST.get('id')
#     remove = request.POST.get('remove')
#     context = {'cart':Wishlist.objects.filter(  username=request.user),'products':[],'cart_items':[],'length':0,'items':'','price':[],'subtotal':0}
#     try :
#         cart_items = WishlistItems.objects.filter(wishlist=context['cart'][0])
#     except IndexError:
#         messages.error(request,'No Items in Cart')
#         return redirect("/products/wishlist/")
    
#     subtotal=0
#     temp = Products.objects.get(product_id=id)
  
#     # to remove
#     if remove=='remove':
#         objects_delete=WishlistItems.objects.filter(wishlist=context['cart'][0]).filter(products_id=temp)
#         print(objects_delete)
#         objects_delete.delete()
#         # return HttpResponseRedirect('cart',context)
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         return redirect("/products/wishlist/")
    
   
#     # context = {
#     #     'previous_url': request.META.get('HTTP_REFERER')
#     # }
#     # return render(request, 'cart/cart.html', context)
#     # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     # return HttpResponseRedirect('cart',context)
#     return redirect("/products/wishlist/")
def updatewishlist(request):
    if request.method == "POST" :#and request.is_ajax():
        # Get the data from the AJAX request
        product_id = request.POST.get("product_id")
        product = Products.objects.get(product_id=product_id)

        wishlist = Wishlist.objects.get(username=request.user) 
        wishlist_object = WishlistItems.objects.get(wishlist=wishlist,products=product)
        wishlist_object.delete()

        data = {}
        data["quantity"]=0
        data["subtotal"]=0
    
        return JsonResponse(data)
    
    # Handle other HTTP methods or non-AJAX requests here
    return HttpResponseBadRequest("Bad Request")

# View cart items :
@login_required
def wishlist(request):
    """
    Shows user the items in the cart.
    """
    id=request.POST.get('id')
    remove = request.POST.get('remove')
    context = {'cart':[],'cart_items':[]}
    context['cart']=Wishlist.objects.filter(username=request.user).first()
    try :
        context['cart_items']=WishlistItems.objects.filter(wishlist=context['cart'])
    except IndexError:
        messages.error(request,'No Items in Cart')
        return render(request,'products/wishlist.html',context)
   
    context['cart_item_quantity'] = len(context["cart_items"])
    return render(request,'products/wishlist.html',context)
