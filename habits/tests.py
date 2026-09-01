from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User(
            email='test@example.com'
        )
        self.user.set_password('testpassword')
        self.user.save()
        self.client.force_authenticate(user=self.user)


    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 1,
            'action_time': 60,
        }
        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'id': 1,
                'place': 'Test place',
                'time': '10:00:00',
                'action': 'Test action',
                'periodicity': 1,
                'reward': None,
                'action_time': 60,
                'public': False,
                'is_pleasant': False,
                'related_habit': None,
            }
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habits(self):
        """Тестирование вывода списка привычек"""
        Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
        )

        response = self.client.get('/habits/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['count'],
            1
        )

    def test_retrieve_habit(self):
        """Тестирование получения одной привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
        )

        response = self.client.get(
            f'/habits/{habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['id'],
            habit.id
        )

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
        )

        data = {
            'place': 'Updated place',
            'time': '11:00:00',
            'action': 'Updated action',
            'periodicity': 1,
            'action_time': 60,
        }

        response = self.client.put(
            f'/habits/{habit.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['place'],
            'Updated place'
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
        )

        response = self.client.delete(
            f'/habits/{habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Habit.objects.filter(id=habit.id).exists()
        )

    def test_reward_and_related_habit(self):
        """Нельзя одновременно указать вознаграждение и связанную привычку"""
        related_habit = Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
            is_pleasant=True,
        )

        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 1,
            'reward': 'Test reward',
            'action_time': 60,
            'related_habit': related_habit.id,
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_action_time_more_than_120(self):
        """Время выполнения не должно превышать 120 секунд"""
        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 1,
            'action_time': 121,
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_related_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной"""
        related_habit = Habit.objects.create(
            user=self.user,
            place='Test place',
            time='10:00:00',
            action='Test action',
            periodicity=1,
            action_time=60,
            is_pleasant=False,
        )

        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 1,
            'action_time': 60,
            'related_habit': related_habit.id,
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_pleasant_habit_cannot_have_reward(self):
        """У приятной привычки не может быть вознаграждения"""
        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 1,
            'reward': 'Test reward',
            'action_time': 60,
            'is_pleasant': True,
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_periodicity_more_than_7(self):
        """Привычка должна выполняться хотя бы один раз в 7 дней"""
        data = {
            'place': 'Test place',
            'time': '10:00:00',
            'action': 'Test action',
            'periodicity': 8,
            'action_time': 60,
        }

        response = self.client.post(
            '/habits/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )