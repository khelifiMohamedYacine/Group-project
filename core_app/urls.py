from django.urls import path
from . import views # Import all views from core_app

from django.shortcuts import redirect

def root_redirect_view(request):
    return redirect('home')

urlpatterns = [
    path('', root_redirect_view), # Redirects / to /home/
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('privacy_policy/', views.privacy_policy_view, name="privacy_policy"),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),

    # Commented for easy removal. Based on group decision
    path('quizzes/', views.quizzes_view, name="quizzes"),
    path('videos/', views.videos_view, name="videos"),
    path('maps/', views.maps_view, name="maps"),
    # End comment
]