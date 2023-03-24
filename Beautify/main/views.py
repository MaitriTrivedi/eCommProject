import math
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View   
from .models import Products,UserData, Cart, CartItems,Coupon,Order,OrderItems,Sellers
from .forms import UserForm, ProductForm, SellerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

session = {'username':''}

# LOGIN :
   
# USER :
def loginPage(request):
    return render(request,'main/login.html')

def loginUser(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=uname, password=password)
        if user:
            if Sellers.objects.filter(user=user).first():
                login(request, user)
                request.session['username']=uname
                return redirect("/adminpage/")
            else:
                login(request, user)
                session['username']=uname
                return redirect("/home/")
        else:
            messages.error(request,"Username or Password Not Valid.")
            return redirect("/login/")
    else:
        return redirect("/login/")

# REGISTER : 

# USER :

def register(request):
    form = UserForm()
    return render (request=request, template_name="main/register.html", context={"register_form":form})

def registerUser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        address=request.POST.get('address')
        contact=request.POST.get('contact')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password2!=password1:
            messages.error(request,"Password didn't match")
            return redirect("/register/")
        if UserData.objects.filter(email=email):
            messages.error(request,"Email already registered.")
            return redirect("/register/")
        # if user with username already registered, then it will create an exception
        try:
            user=User.objects.create_user(username=username,password=password1)
            userD=UserData.objects.create(username=user)
            user.email=userD.email=email
            userD.address=address
            userD.contact=contact
            userD.save()
            user.save()
            context = {username}
            return redirect("/login/")
        except:
            messages.error(request,'User with username already registered')
            return redirect("/register/")
    else:
        return redirect("/register/")

# ADMIN :
def registerAdminForm(request):
    form = SellerForm()
    return render (request=request, template_name="main/adminregister.html", context={"register_form":form})

def adminregister(request):
    if request.method=='POST':
        username=request.POST.get('username')
        company_name=request.POST.get('company_name')
        email=request.POST.get('email')
        address=request.POST.get('address')
        contact=request.POST.get('phone')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password2!=password1:
            messages.error(request,"Password didn't match")
            return redirect("/registerAdminForm/")
        if Sellers.objects.filter(company_name=company_name):
            messages.error(request,"Company already registered.")
            return redirect("/registerAdminForm/")
        # if user with username already registered, then it will create an exception
        try:
            # import pdb;pdb.set_trace()
            user=User.objects.create_user(username=username,password=password1)
            seller=Sellers.objects.create(user=user)
            user.email=email
            seller.address=address
            seller.phone=contact
            seller.company_name=company_name
            seller.save()
            user.save()
            context = {username}
            return redirect("/login/")
        except:
            messages.error(request,'User with username already registered')
            return redirect("/registerAdminForm/")
    else:
        return redirect("/registerAdminForm/")

# LOGOUT :

@login_required
def logoutPage(request):
    # request.session['username']=''
    logout(request)
    return render(request,'main/login.html')

# CART :

@login_required
def updatecart(request):
    # quantity=request.POST.get('quantity')
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

    temp = Products.objects.filter(product_id=id).first()
    if remove=='remove':
        objects_delete=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp)
        objects_delete.delete()
        return HttpResponseRedirect('/cart/',context)
    if sign=='-':
        cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
        cart_objects.quantity=cart_objects.quantity-1
        cart_objects.total_price=cart_objects.total_price-(cart_objects.products.price)
        if cart_objects.quantity==0:
            cart_objects.delete()
        else:
            cart_objects.save()
    if sign=='+':
        cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
        cart_objects.quantity=cart_objects.quantity+1
        cart_objects.total_price=cart_objects.total_price+(cart_objects.products.price)
        cart_objects.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def cart(request):
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

class Category(View):
    def get(self,request,val):
        product = Products.objects.filter(category=val)
        return render(request,'main/category.html',locals())

@login_required
def checkout(request):
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
    return render(request,'main/checkout.html',context)

@login_required
def pay(request):
    context={}
    if request.method=='POST':
        current_user_cart=Cart.objects.filter(username=request.user).first()
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
    return render(request,'main/pay.html',context)

def order(request):
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
    return render(request,'main/order.html',context)

@login_required
def addToCart(request,product_id):
    product = Products.objects.get(product_id=product_id)
    user = request.user
    cart , _ = Cart.objects.get_or_create(username=user,is_paid=False)
    cart.save()
    if CartItems.objects.filter(cart=cart,products=product):
        temp=CartItems.objects.filter(cart=cart,products=product).first()
        temp.quantity = temp.quantity + 1
        temp.total_price= temp.quantity * product.price
        temp.save()
    else:
        cart_items = CartItems.objects.create(cart=cart,products=product)
        cart_items.quantity = 1
        cart_items.total_price= cart_items.quantity * product.price
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)
    request.session['cart'] = cart
    return redirect('cart')

# To view products :
@login_required
def viewProduct(request):
    products = Products.objects.all()
    return render(request,'main/viewProduct.html',{'products':products})

# To add products by the seller
@login_required
def addProduct(request):
    # import pdb;pdb.set_trace()
    context={'seller':request.user}
    form = ProductForm()
    return render (request=request, template_name="main/addProduct.html", context={"product_form":form,'seller':request.user})

@login_required
def addProductToDB(request):
    if request.method=='POST':
        productform=ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            product=productform.save(commit=False)
            seller=Sellers.objects.filter(user=request.user).first()
            product.seller=seller
            product.save()
            return redirect('/viewProduct/')
        else:
            messages.error(request,'Product ID is already registered')
            return redirect('/addProduct/')
    else:
        return redirect('/adminpage/')

# To remove product :

@login_required
def removeProduct(request):
    if request.method=='POST':
        productID = request.POST.get('productID')
        try :
            p = Products.objects.filter(product_id=productID)
            p.delete()
            messages.warning(request, 'Product deleted successfully.')
        except ValueError:
            messages.warning('Productwith product ID {} is not valid...'.format(productID))
    return render (request=request, template_name="main/removeProduct.html")

def removeCartProduct(request):
    if request.method=='POST':
        productID = request.POST.get('productID')
        try :
            p = CartItems.objects.filter(products=productID)
            p.delete()
            messages.warning(request, 'Product deleted successfully.')
        except ValueError:
            messages.warning('Productwith product ID {} is not valid...'.format(productID))
    return render (request=request, template_name="main/removeProduct.html")

# To see user's profile :
@login_required
def myprofile(request,username):
    context={}
    user = User.objects.filter(username =username).first()
    if UserData.objects.filter(username =user).first():
        profile = UserData.objects.get(username =user)
        context['profile']=profile
    else:
        profile2=Sellers.objects.get(user=user)
        context['profile2']=profile2
    return render (request=request, template_name="main/myprofile.html",context=context)

# Home page of admin :
@login_required
def adminpage(request):
    session['username']=request.user
    return render(request,'main/adminpage.html')

# Home page of User :
@login_required
def index(request):
    products= Products.objects.all()
    n= len(products)
    nSlides= n//4 + math.ceil((n/4) + (n//4))
    params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'products': products,'session':session}
    return render(request,'main/index.html',params)

# About page of the site :
def about(request):
    return render(request,'main/about.html')

# Contact page of the site :
def contact(request):
    return render(request,'main/contact.html')

# update product by seller :
@login_required
def updateProduct(request):
    if request.method=='POST':
        productID = request.POST.get('productID')
    try :
        # import pdb; pdb.set_trace()
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
    return render (request=request, template_name="main/updateproduct.html",context={'product':product})

    
        

# Working on :
# @login_required
# def search(request):
#     searchText = request.GET.get('searchText','')
#     products = Products.objects.filter(product_name=searchText)
#     return render(request,'main/search.html',{'products':products})

# def mainHome(request):
#     return render(request,'main/mainHome.html')

# ADMIN login:
# def adminlogin(request):
#     return render (request=request, template_name="main/adminlogin.html")

# def adminloginvalidate(request):
#     if request.method=='POST':
#         uname=request.POST.get('userID')
#         password=request.POST.get('password')
#         user=authenticate(request, username=uname, password=password)
#         if user and Sellers.objects.filter(user=user).first():
#             login(request, user)
#             request.session['username']=uname
#             return redirect("/adminpage/")
#         else:
#             messages.error(request,'You are not a valid AdminUser')
#             return redirect("/adminlogin/")
#     else:
#         return redirect("/adminlogin/")
