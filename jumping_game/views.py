from django.shortcuts import render



def jumping_game_view(request):
    return render(request, 'jumping_game/jumping_game.html')