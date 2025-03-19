from django.urls import path
from . import views



urlpatterns = [
    path("sokoban_game", views.sokoban_game_view, name="sokoban_game"),

    path("admin_pages/sokoban/", views.sokoban_admin_view, name="sokoban_admin"),
    path("admin_pages/sokoban/delete_level/<int:level_number>/", views.delete_level, name="delete_level"),
]

    

