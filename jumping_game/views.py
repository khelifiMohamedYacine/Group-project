import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from core_app.mark_task_complete import mark_task_complete
from .models import JumpingGameLevel

@login_required
def jumping_game_view(request, task_id):

    settings = JumpingGameLevel.objects.filter(id=task_id).first()
    if settings is None:
        return HttpResponse(f"Error: No level found with ID {task_id}", status=404)

    game_data = {
        "speedMultiplier_": settings.speed_multiplier,
        "enemySpawnRate_": settings.enemy_spawn_rate,
        "level_": task_id,
    }
    print(game_data)

    return render(request, 'jumping_game/jumping_game.html', {"game_data": game_data})

@csrf_exempt
@login_required
def mark_jumping_game_complete(request):
    print("try to mark jumping game complete")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")
            reward_pts = data.get("score")

            if not task_id or reward_pts is None:
                return JsonResponse({"error": "Missing task_id or reward_pts"}, status=400)
            user = request.user
            mark_task_complete(user, "JumpingGameLevel", task_id, reward_pts)

            return JsonResponse({"message": f"Level Complete. Recieved {reward_pts} reward points"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)