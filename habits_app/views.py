from rest_framework import generics

from habits_app.models import Habit
from habits_app.paginators import HabitPaginator
from habits_app.permissions import IsOwner
from habits_app.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания привычки.
    """
    serializer_class = HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    """
    Контроллер для вывода списка привычек.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitPublishListAPIView(generics.ListAPIView):
    """
    Контроллер для вывода списка публичных привычек.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_published=True)
    pagination_class = HabitPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра привычки.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования привычки.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления привычки.
    """
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
