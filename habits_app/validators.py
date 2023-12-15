from rest_framework.serializers import ValidationError


class RewardValidator:
    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        related_habit = dict(value).get(self.field_1)
        reward = dict(value).get(self.field_2)
        if related_habit and reward:
            raise ValidationError("У привычки, имеющей связанную привычку, не может быть награды.")
