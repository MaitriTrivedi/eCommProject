from django.shortcuts import render
from cart.models import Cart, CartItems
from django.contrib.auth.decorators import login_required
from orders.models import Order,OrderItems
from django.http import JsonResponse
from products.models import Products

# Create your views here.
# Check order history :
@login_required
def order(request):
    """
    Shows the order history.
    """
    context={'orders':[]}
    context['grandtotal']=[]
    order=Order.objects.filter(username=request.user)
    for i in order :
        t=[]
        temp = OrderItems.objects.filter(order=i)
        if len(temp)>0:
            t.append(i)
            t.append(temp)
            
            sum=0
            for j in temp:
                sum=sum+(j.quantity*j.products.price)
            sum = sum + 100 + sum*(0.18)
            t.append(sum)
            context['orders'].append(t)
    return render(request,'orders/order.html',context)

@login_required
def add_cart_to_orders(request):
    """
    Adds the cart to order history after successful payment.
    """
    # import pdb;pdb.set_trace();
    if request.method == "GET" :
        
        cart = Cart.objects.get(username=request.user)
        cart_item = CartItems.objects.filter(cart=cart)
        data={}
        order = Order.objects.create(username=request.user)
        for i in cart_item:
            temp = OrderItems.objects.create(order=order,products=i.products,quantity=i.quantity,total_price=i.total_price)
            product = Products.objects.get(product_id=i.products.product_id) 
            product.quantity = product.quantity - i.quantity
            product.save()
            i.delete()     
        return JsonResponse(data)
    
    # Handle other HTTP methods or non-AJAX requests here
    return HttpResponseBadRequest("Bad Request")


