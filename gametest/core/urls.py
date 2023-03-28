from django.urls import path
from rest_framework.authtoken import views

from .views import *

urlpatterns = [
    path('api-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('user/', UserView.as_view()),
    path('user/<int:id>/', UpdateDeleteUserView.as_view()),
    path('quiz/<int:id>/play', GameView.as_view()),
    path('quiz/<int:quiz_id>/check_answers/<int:question_id>', CheckAnswersView.as_view()),
    path('quiz/', QuizView.as_view()),
    path('quiz/<int:id>/', QuizDetailView.as_view()),
]
