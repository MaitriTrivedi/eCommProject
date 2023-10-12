from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Sellers, UserData
from .forms import UserForm,SellerForm
from products.models import Products
from products.forms import ProductForm
from main.views import session, isSeller
# session = {'username':'','products':Products.objects.all()}
# Create your views here.

# LOGIN :
   
# USER :
def loginPage(request):
    """
    Displays the login page.
    """
    return render(request,'account/login.html')


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
            try :
                Sellers.objects.get(user=user)
                login(request, user)
                request.session['username']=uname
                return redirect("/acc/adminpage/")
            except ObjectDoesNotExist:
                login(request, user)
                session['username']=uname
                return redirect("/")
        else:
            messages.error(request,"Username or Password Not Valid.")
            return redirect("/acc/login/")
    else:
        return redirect("/acc/login/")

# REGISTER : 
# USER :
def register(request):
    """
    Displays the user-register page.
    """
    form = UserForm()
    return render (request=request, template_name="account/register.html", context={"register_form":form})


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
            return redirect("/acc/register/")
        if UserData.objects.filter(email=email):
            messages.error(request,"Email already registered.")
            return redirect("/acc/register/")
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
            return redirect("/acc/login/")
        except:
            messages.error(request,'User with username already registered')
            return redirect("/acc/register/")
    else:
        return redirect("/acc/register/")


# ADMIN :
def registerAdminForm(request):
    """
    Displays the admin-register page.
    """
    form = SellerForm()
    return render (request=request, template_name="account/adminregister.html", context={"register_form":form})


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
            return redirect("/acc/registerAdminForm/")
        if Sellers.objects.filter(company_name=company_name):
            messages.error(request,"Company already registered.")
            return redirect("/acc/registerAdminForm/")
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
            return redirect("/acc/login/")
        except:
            messages.error(request,'User with username already registered')
            return redirect("/acc/registerAdminForm/")
    else:
        return redirect("/acc/registerAdminForm/")


# LOGOUT :
@login_required
def logoutPage(request):
    """
    Logs the user out and takes the user to login page.
    """
    logout(request)
    return render(request,'main/index.html')

# Home page of admin :
@login_required
def adminpage(request):
    """
    Takes seller to admin page to add, remove or update product.
    """
    session['username']=request.user
    return render(request,'account/adminpage.html')


# To add products by the seller
@login_required
@isSeller
def addProduct(request):
    """
    Adds product by the seller.
    """
    context={'seller':request.user}
    form = ProductForm()
    return render (request=request, template_name="products/addProduct.html", context={"product_form":form,'seller':request.user})

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
            return redirect('/acc/viewProduct/')
        else:
            messages.error(request,'Product ID is already registered')
            return redirect('/acc/addProduct/')
    else:
        return redirect('/acc/adminpage/')


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
            return render(request,'products/updateproduct.html',context)
    return redirect('/viewMyProduct/',context)


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
        return render(request,'products/removeProduct.html',{'products':products})
    else:
        products = Products.objects.all()
        return render(request,'products/viewProduct.html',{'products':products}) 


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
        return render(request,'products/viewMyProduct.html',context)
    except KeyError:
        return redirect('/acc/login/')

# To see user's profile :
@login_required
def myprofile(request,username):
    """
    Shows user profile.
    """
    context={}
    print("====================")
    print(username)
    user = User.objects.get(username=username)
    try:
        UserData.objects.get(username =user)
        profile = UserData.objects.get(username =user)
        context['profile']=profile
    except ObjectDoesNotExist:
        try:
            profile2=Sellers.objects.get(user=user)
            context['profile2']=profile2
        except ObjectDoesNotExist:
            redirect('/acc/login/')
    context['is_edit']=False
    return render (request=request, template_name="account/myprofile.html",context=context)

@login_required
def editProfile(request,username):
    """
    Shows user profile.
    """
    context={}
    print("====================")
    print(username)
    
    try:
        user = User.objects.get(username=username)
        UserData.objects.get(username =user)
        profile = UserData.objects.get(username =user)
        context['profile']=profile
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(username=username)
            profile2=Sellers.objects.get(user=user)
            context['profile2']=profile2
        except ObjectDoesNotExist:
            redirect('/acc/login/')
    context['is_edit']=False
    return render (request=request, template_name="account/edit_profile.html",context=context)

def editProfileSave(request,username):
    """
    Shows user profile.
    """
    context={}
    user = User.objects.get(username=username)
    try:
        UserData.objects.get(username =user)
        profile = UserData.objects.get(username =user)
        context['profile']=profile
    except ObjectDoesNotExist:
        try:
            profile2=Sellers.objects.get(user=user)
            context['profile2']=profile2
        except ObjectDoesNotExist:
            redirect('/acc/login/')
    context['is_edit']=False
    return render (request=request, template_name="account/myprofile.html",context=context)