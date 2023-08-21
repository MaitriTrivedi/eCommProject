from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # user:
    path('mycart/',views.cart,name='cart'),
    path('updatecart/',views.updatecart,name='updatecart'),
    path('addToCart/<product_id>',views.addToCart,name='addToCart'),
  
]
