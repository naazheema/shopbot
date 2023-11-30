from django.contrib import admin
from django.urls import path
from kaspibotapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('testing/', views.testing, name='testing'),
    path('dash/', views.dash, name='dash'),
]