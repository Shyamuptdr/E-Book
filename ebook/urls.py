from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home), 
    path('enquiry/', views.enquiry),    
    
    path('register/', views.register),
    path('verify/', views.verify), 
    path('login/', views.login), 
    
    path('myadmin/', views.adminhome),
    path('manageusers/', views.manageusers),
    path('manageuserstatus/', views.manageuserstatus), 
    path('cpadmin/', views.cpadmin), # change password admin path
    path('mpadmin/', views.mpadmin), # my profile admin path
    path('epadmin/', views.epadmin), # edit profile admin path
    path('viewenquiry/', views.viewenquiry),
    
    path('user/', views.userhome), 
    path('sharenotes/', views.sharenotes),
    path('viewnotes/', views.viewnotes), 
    path('cpusers/', views.cpusers), # change password user path
    path('mpusers/', views.mpusers), # my profile user path
    path('epusers/', views.epusers), # edit profile user path
    
    path('buynotes/', views.buynotes),
    path('payment/', views.payment), 
    path('success/', views.success), 
    path('cancel/', views.cancel) 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
