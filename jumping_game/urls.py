from django.urls import path
from . import views

urlpatterns = [
    path('jumping_game/<int:task_id>/', views.jumping_game_view, name='jumping_game'),

    path('mark_jumping_game_complete/', views.mark_jumping_game_complete, name='mark_jumping_game_complete'),
]