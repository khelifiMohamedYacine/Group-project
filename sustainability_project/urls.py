"""
URL configuration for sustainability_project project.

"""
from django.contrib import admin
from django.urls import path, include

#from core_app import views # tell this file about core_app

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', include('core_app.urls')),  # Include core_app URLs
    path('', include('locations.urls')),
    path('', include('jumping_game.urls')),
    path('', include('sokoban_game.urls')),
    path('', include('quizzes.urls')),
]
