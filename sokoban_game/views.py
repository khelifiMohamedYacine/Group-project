
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from .models import sokoban_results


def sokobanGame(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        level = request.POST.get('level')
        steps = request.POST.get('steps')
        score = request.POST.get('score')
        models.sokoban_results.objects.create(user_id=user_id, level=level, steps=steps, score=score)
    return render(request, 'sokoban_game/SokobanGame-version1.html')


import json
from django.http import JsonResponse
import os

LEVEL_JSON_PATH = os.path.join(os.path.dirname(__file__), "static/game/levels_admin.json")


def sokobanAdmin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            with open(LEVEL_JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return JsonResponse({"message": "Level saved successfully!", "success": True})  # ✅ return JSON
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return render(request, 'sokoban_game/admin.html')

