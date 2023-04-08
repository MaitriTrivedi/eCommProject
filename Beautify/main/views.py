import math

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View   
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Products,UserData, Cart, CartItems,Coupon,Order,OrderItems,Sellers
from .forms import UserForm, ProductForm, SellerForm
from django.shortcuts import redirect
from django.urls import reverse

# decorator :
def isSeller(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))

        # Check if user exists in table
        if not Sellers.objects.filter(user=request.user).exists():
            return redirect(reverse('home'))

        return function(request, *args, **kwargs)
    return wrapper

session = {'username':''}


# LOGIN :
   
# USER :
def loginPage(request):
    """
    Displays the login page.
    """
    return render(request,'main/login.html')

def loginUser(request):
    """
    From the login page,
    if the user is a seller, then logs the user in and takes the user to adminpage.
    if the user is a normal user, then logs the user in and takes the user to home page.
    """
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
                return redirect("/")
        else:
            messages.error(request,"Username or Password Not Valid.")
            return redirect("/login/")
    else:
        return redirect("/login/")

# REGISTER : 
# USER :
def register(request):
    """
    Displays the user-register page.
    """
    form = UserForm()
    return render (request=request, template_name="main/register.html", context={"register_form":form})


def registerUser(request):
    """
    takes the user to the login page.
    """
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
    """
    Displays the admin-register page.
    """
    form = SellerForm()
    return render (request=request, template_name="main/adminregister.html", context={"register_form":form})


def adminregister(request):
    """
    Takes the seller to the login page.
    """
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
    """
    Logs the user out and takes the user to login page.
    """
    logout(request)
    return render(request,'main/login.html')


# To view items category wise :
class Category(View):
    def get(self,request,val):
        product = Products.objects.filter(category=val)
        return render(request,'main/category.html',locals())


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
        return HttpResponseRedirect('/cart/',context)
    
    # to decrease the quantity
    if sign=='-':
        cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
        cart_objects.quantity=cart_objects.quantity-1
        temp.quantity=temp.quantity+1
        temp.save()
        cart_objects.total_price=cart_objects.total_price-(cart_objects.products.price)
        if cart_objects.quantity==0:
            cart_objects.delete()
        else:
            cart_objects.save()

    # to increase the quantity
    if sign=='+':
        cart_objects=CartItems.objects.filter(cart=context['cart'][0]).filter(products_id=temp).first()
        cart_objects.quantity=cart_objects.quantity+1
        temp.quantity=temp.quantity-1
        temp.save()
        cart_objects.total_price=cart_objects.total_price+(cart_objects.products.price)
        cart_objects.save()
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
    return render(request,'main/checkout.html',context)

# pay :
@login_required
def pay(request):
    """
    Starts the payment process.
    """
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
    return render(request,'main/order.html',context)


# To view products :
@login_required
def viewProduct(request):
    """
    Shows all the products.
    """
    if request.POST.get('value')=='admin':
        temp1 =User.objects.get(username=request.session['username'])
        temp2=Sellers.objects.get(user=temp1)
        products = Products.objects.filter(seller=temp2)
        return render(request,'main/removeProduct.html',{'products':products})
    else:
        products = Products.objects.all()
        return render(request,'main/viewProduct.html',{'products':products}) 


# To view product in detail :
@login_required
def view(request,id):
    """
    Shows the particular product in detail.
    """
    product = Products.objects.get(product_id=id)
    return render(request,'main/view.html',{'product':product})


# To add products by the seller
@login_required
@isSeller
def addProduct(request):
    """
    Adds product by the seller.
    """
    context={'seller':request.user}
    form = ProductForm()
    return render (request=request, template_name="main/addProduct.html", context={"product_form":form,'seller':request.user})

@login_required
@isSeller
def addProductToDB(request):
    """
    Saves the added product to database for further operations.
    """
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


# To view products for seller :
@login_required
@isSeller
def viewMyProduct(request):
    """
    Shows all the products added by that particular seller.
    """
    context={}
    try:
        temp1 =Sellers.objects.get(user=User.objects.get(username=request.session['username']))
        context['products'] = Products.objects.filter(seller=temp1)
        context['admin']=request.user
        return render(request,'main/viewMyProduct.html',context)
    except KeyError:
        return redirect('/login/')


# To update my products :
@login_required
@isSeller
def updateMyProduct(request):
    """
    Enables the seller to update or remove the product.
    """
    context={}
    if request.method=='POST':
        removeOrUpdate=request.POST.get('removeOrUpdate')
        id=request.POST.get('productID')
        admin=request.POST.get('admin')
        context['admin']=request.user
        context['id']=id
        if removeOrUpdate=='remove':
            product=Products.objects.get(product_id=id)
            product.delete()
        if removeOrUpdate=='update':
            p = Products.objects.get(product_id=id)
            product = ProductForm(instance=p)
            context['product']=product
            context['id']=id
            return render(request,'main/updateproduct.html',context)
    return redirect('/viewMyProduct/',context)


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
    return render (request=request, template_name="main/updateproduct.html",context={'product':product})


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
    return render (request=request, template_name="main/updateproduct.html",context={'product':product})


# To see user's profile :
@login_required
def myprofile(request,username):
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
    return render (request=request, template_name="main/myprofile.html",context=context)


# Home page of admin :
def adminpage(request):
    """
    Takes seller to admin page to add, remove or update product.
    """
    session['username']=request.user
    return render(request,'main/adminpage.html')


# Home page of User :
@login_required
def index(request):
    """
    Takes user to home page.
    """
    products= Products.objects.all()
    n= len(products)
    nSlides= n//4 + math.ceil((n/4) + (n//4))
    params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'products': products,'session':session}
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
