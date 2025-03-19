from django.urls import path
from .views import jumping_game_view  # Import the new view

urlpatterns = [
    path('jumping_game/', jumping_game_view, name='jumping_game'),
]