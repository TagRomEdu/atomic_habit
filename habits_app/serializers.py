from rest_framework import serializers

from habits_app.models import Habit
from habits_app.validators import RewardPleasantValidator, TimeValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RewardPleasantValidator(field_1='related_habit', field_2='reward', field_3='is_pleasant'),
                      TimeValidator(field_1='time_required')]
