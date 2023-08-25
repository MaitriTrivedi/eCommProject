import math


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View   

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from account.models import UserData
from products.models import Products
from orders.models import Order, OrderItems
from .models import Coupon
from .forms import UserForm, SellerForm
from django.shortcuts import redirect
from django.urls import reverse

from cart.models import Cart, CartItems
from account.models import Sellers

# decorator :
def isSeller(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))

        # Check if user exists in table
        if not Sellers.objects.filter(user=request.user).exists():
            return redirect(reverse('index'))

        return function(request, *args, **kwargs)
    return wrapper

session = {'username':'','products':Products.objects.all()}



# To view items category wise :
class Category(View):
    def get(self,request,val):
        product = Products.objects.filter(category=val)
        return render(request,'main/category.html',locals())


# # CART :
# # Add product to cart :
# @login_required
# def addToCart(request,product_id):
#     """
#     Adds product to user's cart.
#     """
#     product = Products.objects.get(product_id=product_id)
#     user = request.user
#     cart , _ = Cart.objects.get_or_create(username=user,is_paid=False)
#     cart.save()
#     if CartItems.objects.filter(cart=cart,products=product):
#         temp=CartItems.objects.filter(cart=cart,products=product).first()
#         temp.quantity = temp.quantity + 1
#         product.quantity=product.quantity-1
#         product.save()
#         temp.total_price= temp.quantity * product.price
#         temp.save()
#     else:
#         cart_items = CartItems.objects.create(cart=cart,products=product)
#         cart_items.quantity = 1
#         product.quantity=product.quantity-1
#         product.save()
#         cart_items.total_price= cart_items.quantity * product.price
#         cart_items.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# # Update cart :
# @login_required
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
#         return render(request,'cart/cart.html',context)
#     subtotal=0
#     temp = Products.objects.get(product_id=id)

#     # to remove
#     if remove=='remove':
#         objects_delete=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp)
#         temp.quantity=temp.quantity+objects_delete[0].quantity
#         temp.save()
#         objects_delete.delete()
#         return HttpResponseRedirect('/cart/',context)
    
#     # to decrease the quantity
#     if sign=='-':
#         try :
#             cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
#             cart_objects.quantity=cart_objects.quantity-1
#         except CartItems.DoesNotExist:
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
#         except CartItems.DoesNotExist:
#             cart_objects.quantity = 1
        
#         temp.quantity=temp.quantity-1
#         temp.save()
#         cart_objects.total_price=cart_objects.total_price+(cart_objects.products.price)
#         cart_objects.save()

#     # context = {
#     #     'previous_url': request.META.get('HTTP_REFERER')
#     # }
#     # return render(request, 'cart/cart.html', context)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# # View cart items :
# @login_required
# def cart(request):
#     """
#     Shows user the items in the cart.
#     """
#     sign = request.POST.get('sign')
#     id=request.POST.get('id')
#     remove = request.POST.get('remove')
#     context = {'cart':[],'cart_items':[]}
#     context['cart']=Cart.objects.filter(is_paid=False,username=request.user).first()
#     try :
#         context['cart_items']=CartItems.objects.filter(cart=context['cart'])
#     except IndexError:
#         messages.error(request,'No Items in Cart')
#         return render(request,'orders/order.html',context)
#     totalQuantity=0
#     totalCost=0
#     for i in range(len(context['cart_items'])):
#         totalCost=totalCost+(context['cart_items'][i].quantity*context['cart_items'][i].products.price)
#         totalQuantity=totalQuantity+(context['cart_items'][i].quantity)
#     context['subtotal']=totalCost
#     context['tax']=totalCost*(0.18)
#     context['grandtotal']=totalCost+100+context['tax']
#     return render(request,'cart/cart.html',context)


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



# To view product in detail :
@login_required
def view(request,id):
    """
    Shows the particular product in detail.
    """
    product = Products.objects.get(product_id=id)
    return render(request,'main/view.html',{'product':product})







@login_required
@isSeller
def updateEach(request,id):
    """
    Shows the updateProduct page with prefilled fields.
    """
    try:
        p = Products.objects.get(product_id=int(id))
        product = ProductForm(request.POST or None, instance=p)
        if request.method == 'POST' and product.is_valid():
            p.product_name = product.cleaned_data['product_name']
            p.price = product.cleaned_data['price']
            p.description = product.cleaned_data['description']
            p.category = product.cleaned_data['category']
            p.quantity = product.cleaned_data['quantity']
            p.product_image = product.cleaned_data['product_image']
            p.save()
            return redirect('/viewMyProduct/')
        else:
            messages.error(request,'You are not authorised for this product')
            return redirect('/viewMyProduct/')
    except ValueError:
        messages.warning('Productwith product ID is not valid...')
    return render (request=request, template_name="products/updateproduct.html",context={'product':product})


# update product by seller :
@login_required
@isSeller
def updateProduct(request):
    """
    For updating selected item from the updateMyProduct view and save them to the database.
    """
    if request.method=='POST':
        productID = request.POST.get('productID')
    try :
        p = Products.objects.filter(product_id=productID)
        p.delete()
        product=ProductForm(request.POST,request.FILES)
        if product.is_valid():
            temp=product.save(commit=False)
            product.product_id=productID
            seller=Sellers.objects.filter(user=request.user).first()
            if p.seller==seller:
                product.seller=seller
                product.save()
                return redirect('/viewProduct/')
            else:
                messages.error('You are not authorised for this product')
                return redirect('/updateproduct/')
    except ValueError:
        messages.warning('Productwith product ID {} is not valid...'.format(productID))
    return render (request=request, template_name="products/updateproduct.html",context={'product':product})



def edit_myprofile(request,username):
    """
    Shows user profile.
    """
    context={}
    user = User.objects.filter(username =username).first()
    if UserData.objects.filter(username =user).first():
        profile = UserData.objects.get(username =user)
        context['profile']=profile
    else:
        profile2=Sellers.objects.get(user=user)
        context['profile2']=profile2
    context['is_edit']=True
    return render (request=request, template_name="account/myprofile.html",context=context)


# Home page of User :
# @login_required
def index(request):
    """
    Takes user to home page.
    """
    products= Products.objects.all()
    n= len(products)
    nSlides= n//4 + math.ceil((n/4) + (n//4))
    
    cart_count = 0
    if not request.user.is_anonymous :
        print(request.user)
        cart=Cart.objects.get(username=request.user)
        cart_items = CartItems.objects.filter(cart=cart)
        for i in cart_items :
            cart_count =cart_count + i.quantity
    else :
        cart_count = 0
    params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'products': products,'session':session,'cart_count':cart_count}
    return render(request,'main/index.html',params)


# About page of the site :
def about(request):
    """
    Takes user to about page.
    """
    return render(request,'main/about.html')


# Contact page of the site :
def contact(request):
    """
    Takes user to contact page.
    """
    return render(request,'main/contact.html')

