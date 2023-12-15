from rest_framework.serializers import ValidationError


class RewardPleasantValidator:
    def __init__(self, field_1, field_2, field_3):
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def __call__(self, value):
        related_habit = dict(value).get(self.field_1)
        reward = dict(value).get(self.field_2)
        is_pleasant = dict(value).get(self.field_3)
        if is_pleasant:
            if reward:
                raise ValidationError("У приятной привычки не может быть награды.")
        if related_habit:
            if reward:
                raise ValidationError("У привязываемой привычки не может быть награды.")
            if not is_pleasant:
                raise ValidationError("Чтобы связать привычку, она должна быть приятной.")


class TimeValidator:
    def __init__(self, field_1):
        self.field_1 = field_1

    def __call__(self, value):
        time = dict(value).get(self.field_1)
        if int(time) > 120:
            raise ValidationError("Время выполнения привычки не должно быть более 120 секунд, капуша!")
