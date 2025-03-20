from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import jumping_game_level


def jumping_game_view(request):
    return render(request, 'jumping_game/jumping_game.html')

def jumping_game_view(request, task_id):

    settings = jumping_game_level.objects.filter(id=task_id).first()
    if settings is None:
        return HttpResponse(f"Error: No level found with ID {task_id}", status=404)

    game_data = {
        "speedMultiplier_": settings.speed_multiplier,
        "enemySpawnRate_": settings.enemy_spawn_rate,
        "level_": task_id,
    }
    print(game_data)

    return render(request, 'jumping_game/jumping_game.html', {"game_data": game_data})