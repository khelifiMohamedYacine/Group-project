from django.urls import path

from . import views

#app_name = "quiz"

urlpatterns = [
    path("quiz/", views.quiz_view, name="quiz"),
    path("quiz_results/", views.quiz_results_view, name="quiz_results"),
]
