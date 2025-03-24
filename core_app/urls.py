from django.urls import path
from . import views # Import all views from core_app

from django.shortcuts import redirect

def root_redirect_view(request):
    return redirect('home') # May revert back to home

urlpatterns = [
    path('', root_redirect_view), # Redirects / to /home/
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('privacy_policy/', views.privacy_policy_view, name="privacy_policy"),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('games/', views.games_view, name="games_page"),
    path('videos/', views.videos_view, name="videos"),

    # admin only urls
    path('game_admin/dashboard/', views.admin_view, name="admin_dashboard"),
    path('game_admin/content/', views.admin_content_view, name="admin_content"),
    path('game_admin/users/', views.admin_users_view, name="admin_users"),
    path('game_admin/analytics/', views.admin_analytics_view, name="admin_analytics"),
    path('game_admin/quiz/', views.admin_quiz_view, name="admin_quiz"),
    path('game_admin/jumping/', views.admin_jumping_view, name="admin_jumping"),
]