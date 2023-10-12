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
    path('adminpage/',views.adminpage,name='adminpage'),
  
    path('add-product-to-db/',views.addProductToDB,name='addItemToDB'),
    path('addProduct/',views.addProduct,name='addProduct'),
    path('updateMyProduct/',views.updateMyProduct,name='updateMyProduct'),

    #view products : 
    path('viewProduct/',views.viewProduct,name='viewProduct'),
    path('viewMyProduct/',views.viewMyProduct,name='viewMyProduct'),

    path('myprofile/<str:username>',views.myprofile,name='myprofile'),
    path('myprofile/edit/<str:username>',views.editProfile,name='editProfile'),
    path('myprofile/edit_save/<str:username>',views.editProfileSave,name='editProfileSave')
]