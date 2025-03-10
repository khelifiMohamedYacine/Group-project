from django.urls import path
from . import views



urlpatterns = [
    path('sokoban_game', views.sokobanGame, name='SokobanGame'),

    path('game_admin/sokoban/', views.sokobanAdmin, name='SokobanAdmin'),

]
