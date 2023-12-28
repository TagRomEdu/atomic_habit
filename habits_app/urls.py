from django.urls import path

from habits_app.apps import HabitsAppConfig
from habits_app.views import HabitCreateAPIView, HabitListAPIView, \
    HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, HabitPublishListAPIView

app_name = HabitsAppConfig.name

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='create_habit'),
    path('list/', HabitListAPIView.as_view(), name='list_habit'),
    path('list/publish/', HabitPublishListAPIView.as_view(),
         name='publish_list_habit'),
    path('retrieve/<int:pk>', HabitRetrieveAPIView.as_view(),
         name='retrieve_habit'),
    path('update/<int:pk>', HabitUpdateAPIView.as_view(),
         name='update_habit'),
    path('destroy/<int:pk>', HabitDestroyAPIView.as_view(),
         name='destroy_habit'),
]
