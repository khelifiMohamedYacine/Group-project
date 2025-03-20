from django.urls import path
from . import views



urlpatterns = [
    path("sokoban_game/<int:task_id>/", views.sokoban_game_view, name="sokoban_game"),

    #path("game_admin/sokoban/", views.sokoban_admin_view, name="sokoban_admin"),
    path("game_admin/sokoban/delete_level/<int:level_number>/", views.delete_level, name="delete_level"),
]

    

