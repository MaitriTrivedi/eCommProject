from django.urls import path, include
from . import views

urlpatterns = [
    path('wishlist/',views.wishlist,name='wishlist'),
    path('updatewishlist/',views.updatewishlist,name='updatewishlist'),
    path('add_to_wishlist/<product_id>',views.addtowishlist,name='add_to_wishlist'),
]
