from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings


NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIOD_HOURLY = 'hourly'
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'

    PERIODS = (
        (PERIOD_HOURLY, 'Ежечасно'),
        (PERIOD_DAILY, 'Ежедневно'),
        (PERIOD_WEEKLY, 'Еженедельно')
    )

    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(_("place"), max_length=200)
    time = models.TimeField(_("time"))
    activity = models.TextField(_("activity"))
    is_pleasant = models.BooleanField(_("pleasant habit"), default=False)
    related_habit = models.ForeignKey(to='self', on_delete=models.CASCADE, **NULLABLE, related_name='related_set')
    period = models.CharField(_("period"), max_length=50, choices=PERIODS, default=PERIOD_DAILY)
    reward = models.TextField(_("reward"), **NULLABLE)
    time_required = models.PositiveSmallIntegerField(_("time required in seconds"), default=120)
    is_published = models.BooleanField(_("published"), default=False)

    def __str__(self):
        return f'{self.pk} - {self.activity}'

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
