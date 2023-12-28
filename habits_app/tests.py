from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits_app.models import Habit
from users_app.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        """
        Метод для установки тестовых данных.
        """
        self.client = APIClient()

        # Создание тестовых аккаунтов
        self.user = User.objects.create(
            email='test@test.ru',
            password='test',

            is_active=True,
        )

        self.another_user = User.objects.create(
            email='testik@test.ru',
            password='testik',

            is_active=True,
        )

        # Аутентификация тестового аккаунта
        self.client.force_authenticate(user=self.user)

        # Создание тестовых привычек
        self.habit = Habit.objects.create(
            owner=self.user,
            place="world",
            time='00:00:00',
            activity="say hello",
            is_pleasant=False,
            related_habit=None,
            reward=None,
            time_required=1,
            is_published=True,
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="dream",
            time='00:00:00',
            activity="say goodbye",
            is_pleasant=True,
            related_habit=None,
            reward=None,
            time_required=1,
            is_published=False,
        )

        self.another_habit = Habit.objects.create(
            owner=self.another_user,
            place="home",
            time='00:00:00',
            activity="say nothing",
            is_pleasant=False,
            related_habit=None,
            reward=None,
            time_required=1,
            is_published=False,
        )

    def tearDown(self):
        """
        Метод cброса тестовых данных.
        """

        # Удаляет всех пользователей и привычки
        User.objects.all().delete()
        Habit.objects.all().delete()
        super().tearDown()

        # Подключение к тесовой базе данных
        with connection.cursor() as cursor:
            # Сброс идентификаторов пользователей и привычек
            cursor.execute("""
                SELECT setval(pg_get_serial_sequence(
                           '"users_app_user"','id'), 1, false);
                SELECT setval(pg_get_serial_sequence(
                           '"habits_app_habit"','id'), 1, false);
            """)

    def test_get_habit_list(self):
        """
        Тест для получения списка полезных привычек.
        """

        response = self.client.get(
            reverse('habits_app:list_habit')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_retrieve(self):
        """
        Тест для получения существующей привычки.
        """

        response = self.client.get(
            reverse('habits_app:retrieve_habit', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_another_habit_retrieve(self):
        """
        Тест для получения существующей привычки другого пользователя.
        """

        response = self.client.get(
            reverse('habits_app:retrieve_habit',
                    kwargs={'pk': self.another_habit.pk}
                    ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_create(self):
        """
        Тестирование создания привычки пользователем (валидными данными).
        """
        data = {
            "owner": self.user.pk,
            "place": "shop",
            "time": "09:35",
            "activity": "battle",
            "time_required": 100
            }

        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_invalid_habit_create(self):
        """
        Тестирование создания привычки пользователем (невалидными данными).
        """

        data = {
            "owner": self.user.pk,
            "place": "shop",
            "time": "09:35",
            "activity": "battle",
            "time_required": 1000
            }

        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_habit_update(self):
        """
        Тестирование обновления привычки пользователем (валидными данными).
        """

        data = {
            "owner": self.user.pk,
            "place": "underdark",
            "time": "13:13",
            "activity": "to fear or not to fear",
            "time_required": 100
        }

        response = self.client.put(
            reverse('habits_app:update_habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        wished_answer = {'id': 1, 'place': 'underdark', 'time': '13:13:00',
                         'activity': 'to fear or not to fear',
                         'is_pleasant': False, 'period': 'daily',
                         'reward': None, 'time_required': 100,
                         'is_published': False, 'owner': 1,
                         'related_habit': None
                         }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_habit_update(self):
        """
        Тестирование обновления привычки пользователем (невалидными данными).
        """

        data = {
            "place": "underdark",
            "time": "13:13",
            "activity": "to fear or not to fear",
        }

        response = self.client.put(
            reverse('habits_app:update_habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_another_habit_update(self):
        """
        Тестирование обновления привычки другого пользователя.
        """

        data = {
            "owner": self.user.pk,
            "place": "underdark",
            "time": "13:13",
            "activity": "to fear or not to fear",
            "time_required": 100
        }

        response = self.client.put(
            reverse('habits_app:update_habit',
                    kwargs={'pk': self.another_habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_patch(self):
        """
        Тестирование частичного обновления привычки пользователем
        (валидными данными).
        """

        data = {
            "place": "underdark",
            "time_required": 100
        }

        response = self.client.patch(
            reverse('habits_app:update_habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        wished_answer = {'id': 1, 'place': 'underdark', 'time': '00:00:00',
                         'activity': 'say hello', 'is_pleasant': False,
                         'period': 'daily', 'reward': None,
                         'time_required': 100, 'is_published': True,
                         'owner': 1, 'related_habit': None}

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            wished_answer
        )

    def test_invalid_habit_patch(self):
        """
        Тестирование частичного обновления привычки пользователем
        (невалидными данными).
        """

        data = {
            "time_required": 1000
        }

        response = self.client.patch(
            reverse('habits_app:update_habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_another_habit_patch(self):
        """
        Тестирование частичного обновления привычки другого пользователя.
        """

        data = {
            "place": "underdark",
            "time_required": 100
        }

        response = self.client.put(
            reverse('habits_app:update_habit',
                    kwargs={'pk': self.another_habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_habit_delete(self):
        """
        Тестирование удаления привычки пользователем (валидными данными).
        """

        response = self.client.delete(
            reverse('habits_app:destroy_habit', kwargs={'pk': self.habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_another_habit_delete(self):
        """
        Тестирование удаления привычки другого пользователя.
        """

        response = self.client.delete(
            reverse('habits_app:destroy_habit',
                    kwargs={'pk': self.another_habit.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_publish_habit_list(self):
        """
        Тест на получение списка публичных привычек.
        """

        response = self.client.get(
            reverse('habits_app:publish_list_habit')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_related_or_reward_validator(self):
        """
        Тест валидатора RewardPleasantValidator.
        Проверка, на то, что:
            - нельзя выбрать одновременно вознаграждение и связанную привычку.
        """

        data = {'id': 5,
                'place': 'underdark',
                'time': '13:13:00',
                'activity': 'to fear or not to fear',
                'is_pleasant': True,
                'period': 'daily',
                'reward': "GLOOORYYY",
                'time_required': 100,
                'is_published': False,
                'owner': 1,
                }

        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                'У приятной привычки не может быть награды.'
                ]
             }
        )

    def test_check_related_validator(self):
        """
        Тест валидатора RewardPleasantValidator.
        Проверка, на то, что:
            - у связанной привычки не может быть награды.
        """

        data = {'id': 5,
                'place': 'underdark',
                'time': '13:13:00',
                'activity': 'to fear or not to fear',
                'is_pleasant': False,
                'period': 'daily',
                'reward': "GLOOORYYY",
                'time_required': 100,
                'is_published': False,
                'owner': 1,
                'related_habit': 1
                }

        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                'У привязываемой привычки не может быть награды.'
                ]
             }
        )

    def test_check_pleasant_validator(self):
        """
        Тест валидатора RewardPleasantValidator.
        Проверка, на то, что:
             - связываемая привычка должна быть приятной.
        """

        data = {'id': 5,
                'place': 'underdark',
                'time': '13:13:00',
                'activity': 'to fear or not to fear',
                'is_pleasant': False,
                'period': 'daily',
                'time_required': 100,
                'is_published': False,
                'owner': 1,
                'related_habit': 1
                }

        response = self.client.post(
            reverse('habits_app:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                'Чтобы связать привычку, она должна быть приятной.'
                ]
             }
        )

    def test_check_time_validator(self):
        """
        Тест валидатора TimeValidator, проверяющего,
        что время выполнения должно быть не больше 120 секунд.
        """

        data = {
            "time_required": 1000
        }

        response = self.client.patch(
            reverse('habits_app:update_habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                'Время выполнения привычки не должно быть более 120 секунд, '
                'капуша!'
            ]}
        )
