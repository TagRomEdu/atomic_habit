from rest_framework import serializers

from habits_app.models import Habit
from habits_app.validators import RewardValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RewardValidator(field_1='related_habit', field_2='reward')]
