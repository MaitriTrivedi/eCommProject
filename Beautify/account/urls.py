from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # login :
    path('login/',views.loginPage,name='login'),# user
    path('login-user/',views.loginUser,name='login user'),# user

    #logout :
    path('logout/',views.logoutPage,name='logout'),

 
    path('register/',views.register,name='register'),
    path('registerAdminForm/',views.registerAdminForm,name='registerAdminForm'),
    path('register-user/',views.registerUser,name='registerUser'),
    # # path('update_cart/<int:product_id>/', views.update_cart, name='updateCart'),
    path('adminregister/',views.adminregister,name='adminregister'),
  
]