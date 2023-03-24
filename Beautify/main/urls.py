from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # login :
    path('login/',views.loginPage,name='login'),# user
    path('login-user/',views.loginUser,name='login user'),# user
    # path('adminlogin/',views.adminlogin,name='adminlogin'),# admin
    # path('admin-login-validate/',views.login,name='adminlogin'),# admin

    #logout :
    path('logout/',views.logoutPage,name='logout'),

    #view products : 
    path('viewProduct/',views.viewProduct,name='viewProduct'),
    path('category/<slug:val>',views.Category.as_view(),name='category'), # viewproducts categorywise

    #extra pages:
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    # path('search/',views.search,name='search'),

    # user:
    path('cart/',views.cart,name='cart'),
    path('updatecart/',views.updatecart,name='updatecart'),
    path('checkout/',views.checkout,name='checkout'),
    path('pay/',views.pay,name='pay'),
    path('order/',views.order,name='order'),
    path('myprofile/<str:username>',views.myprofile,name='myprofile'),
    path('addToCart/<product_id>',views.addToCart,name='addToCart'),

    # admin user :
    path('adminpage/',views.adminpage,name='adminpage'), # admin Home page
    path('add-product-to-db/',views.addProductToDB,name='addItemToDB'),
    path('addProduct/',views.addProduct,name='addProduct'),
    path('removeProduct/',views.removeProduct,name='removeProduct'),
    path('updateProduct/',views.updateProduct,name='updateProduct'),

    # working :
    path('home/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('registerAdminForm/',views.registerAdminForm,name='registerAdminForm'),
    path('register-user/',views.registerUser,name='registerUser'),
    # path('mainHome/',views.mainHome,name='mainHome'),
    path('update_cart/<int:product_id>/', views.update_cart, name='updateCart'),

    # path('removeCartProduct/',views.removeCartProduct,name='removeCartProduct'),
    path('adminregister/',views.adminregister,name='adminregister'),
    # path('main/',views.main,name='main'),
    # path('register/',views.register,name='register'),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)