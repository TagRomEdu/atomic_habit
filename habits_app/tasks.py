import requests
import time
from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from habits_app.models import Habit
from users_app.models import User


WEEKDAY = {
    0: 'monday',
    1: 'tuesday',
    2: 'wednesday',
    3: 'thursday',
    4: 'friday',
    5: 'saturday',
    6: 'sunday',
}


@shared_task
def get_tg_user_id():
    """
    Периодическая задача для просмотра логов бота, чтобы достать id Юзера.
    """

    for user in User.objects.filter(~Q(telegram=None)):

        response = requests.get(
            f'{settings.TG_URL}/bot{settings.TG_BOT_API}/getUpdates'
            ).json()
        user_id = next(
            (item["message"]["from"]["id"] for item in response["result"]
             if item["message"]["from"]["username"] == user.telegram), None
             )

        if user_id:
            user.tg_id = user_id
            user.save()


@shared_task
def tg_integration():
    """
    Периодическая задача для отправки уведомления о привычке в tg.
    """

    date_time = timezone.datetime.now()
    weekday = date_time.date().weekday()

    # Получаем время в UTC
    utc_time = list(time.strftime("%H:%M", time.localtime(time.time())))
    utc_time[1] = str(int(utc_time[1]) + 3)  # Переводим в Московское
    habit_time = ''.join(utc_time)  # Превращаем обратно в строку

    habits = Habit.objects.filter(time=habit_time,
                                  period__in=[
                                      WEEKDAY[weekday],
                                      'daily',
                                      'hourly'
                                      ]
                                  )

    if habits:
        for habit in habits:
            if habit.owner.tg_id:
                params = {
                    'chat_id': habit.owner.tg_id,
                    'text': habit
                }
                requests.post(
                    f'{settings.TG_URL}/bot{settings.TG_BOT_API}/sendMessage',
                    params=params
                    )
