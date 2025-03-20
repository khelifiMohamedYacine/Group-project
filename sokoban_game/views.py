import json
from django.shortcuts import render

from django.http import JsonResponse

from sokoban_game.models import sokoban_level, sokoban_results

from django.views.decorators.csrf import csrf_exempt #temp

@csrf_exempt
def sokoban_game_view(request, task_id):
    # Note that the sokoban javascript was designed to take an array of every sokoban level and play each in sequence
    # But it was decided that users would only play one level at a time. To avoid major changes to the javascript this
    # view now just returns an array of only one level. I guess this is minor tech debt

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        level = request.POST.get('level')
        steps = request.POST.get('steps')
        score = request.POST.get('score')
        sokoban_results.objects.create(user_id=user_id, level_id=level, steps=steps)

    level = sokoban_level.objects.filter(id=task_id).first()  # Fetch the level using task_id
    if not level:
        # Handle case if the level with the given task_id doesn't exist, Doesnt work :(
        return render(request, 'sokoban_game/SokobanGame-version1.html', {"error": "Level not found."})
    levels_list = []
    levels_list.append({
        "number": task_id,
        "map_data": json.loads(level.map_data),
        "box_positions": json.loads(level.box_positions),
        "person_position": json.loads(level.person_position)  
    })
    return render(request, 'sokoban_game/SokobanGame-version1.html', {"levels": json.dumps(levels_list)})


@csrf_exempt
def sokoban_admin_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for level_data in data:
                level, created = sokoban_level.objects.update_or_create(
                    number=level_data["number"],
                    defaults={
                        "map_data": json.dumps(level_data["map_data"]),
                        "box_positions": json.dumps(level_data["box_positions"]),
                        "person_position": json.dumps(level_data["person_position"])
                    }
                )

            return JsonResponse({"message": "Levels updated successfully!", "success": True})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    levels = sokoban_level.objects.all().values("number", "map_data", "box_positions", "person_position")
    levels_list = []
    for level in levels:
        levels_list.append({
            "number": level["number"],
            "map_data": json.loads(level["map_data"]),
            "box_positions": json.loads(level["box_positions"]),
            "person_position": json.loads(level["person_position"])
        })

    return render(request, 'sokoban_game/admin.html', {"levels": json.dumps(levels_list)})

@csrf_exempt
def delete_level(request, level_number):
    if request.method == "DELETE":
        try:
            level = sokoban_level.objects.get(number=level_number)
            level.delete()
            print("del success")
            return JsonResponse({"success": True, "message": f"Level {level_number} deleted successfully!"})
            
        except sokoban_level.DoesNotExist:
            print("del fail")
            return JsonResponse({"success": False, "error": "Level not found."})
        print("del how did we get here")
    print("del or here")
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
