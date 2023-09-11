from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('category/<slug:val>',views.Category.as_view(),name='category'), # viewproducts categorywise
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('view/<id>',views.view,name='view'),
    path('updateEach/<id>',views.updateEach,name='updateEach'),
    path('search/',views.search_view,name="search_view"),
    
    path('',views.index,name='index'),
]   

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)