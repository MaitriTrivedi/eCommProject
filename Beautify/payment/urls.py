from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pay/',views.pay,name='pay'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('pay/return_view/',views.return_view,name='return_view'),
    path('pay/cancel_view/',views.cancel_view,name='cancel_view'),
    path('checkout/',views.checkout,name='checkout'),
]   
