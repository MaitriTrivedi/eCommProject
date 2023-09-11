from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/',views.order,name='order'),
    path('add_order', views.add_cart_to_orders, name='addOrder')
]   
