from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path('quiz/<int:task_id>/', views.quiz_view, name='quiz'),
    path("quiz_results/", views.quiz_results_view, name="quiz_results"),
]
