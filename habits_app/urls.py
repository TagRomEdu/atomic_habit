from django.urls import path

from habits_app.apps import HabitsAppConfig
from habits_app.views import HabitCreateAPIView


app_name = HabitsAppConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create_habit')
]
