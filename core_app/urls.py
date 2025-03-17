from django.urls import path
from . import views # Import all views from core_app

from django.shortcuts import redirect

def root_redirect_view(request):
    return redirect('register') # May revert back to home

urlpatterns = [
    path('', root_redirect_view), # Redirects / to /home/ # Actually register
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('privacy_policy/', views.privacy_policy_view, name="privacy_policy"),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('content/', views.content_manage, name="content_manage"),
    path('admin_dashboard/', views.admin_view, name="admin_dashboard"),
    path('games/', views.games_view, name="games_page"),

    # Commented for easy removal. Based on group decision
    path('videos/', views.videos_view, name="videos"),
    path('maps/', views.maps_view, name="maps"),
    # End comment
    path('analyse/', views.analyse_users, name='analyse_users'),
    path('users/', views.manage_users, name='manage_users'),

]
