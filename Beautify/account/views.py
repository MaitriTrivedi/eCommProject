from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from .models import Sellers, UserData
from .forms import UserForm,SellerForm
from products.models import Products
from main.views import session
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
            if Sellers.objects.filter(user=user).first():
                login(request, user)
                request.session['username']=uname
                return redirect("/adminpage/")
            else:
                login(request, user)
                print(uname)
                session['username']=uname
                print(session['username'])
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
