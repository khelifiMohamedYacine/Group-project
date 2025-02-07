from django.urls import path
from . import views  # Import all views from core_app
from .views import logout_view  # Import the logout view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]