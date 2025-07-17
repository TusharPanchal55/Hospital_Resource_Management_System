from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_login_view
from django.contrib.auth.decorators import login_required
from .mongo import usage_collection
from django.utils import timezone
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('add_data/', views.add_view, name='add'),
    path('list/', views.list_view, name='list'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', custom_login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', custom_login_view, name='logout'),
]
