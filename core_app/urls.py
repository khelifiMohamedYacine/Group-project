from django.urls import path
from . import views # Import all views from core_app
from .views import logout_view  # Import the logout view

from django.shortcuts import redirect

def root_redirect_view(request):
    return redirect('home')

urlpatterns = [
    path('', root_redirect_view), # Redirects / to /home/
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]