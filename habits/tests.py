import json

from django.urls import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitsAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email="test@test.com", tg_id="123456789")

        # Создаем привычку для этого пользователя
        self.habit = Habit.objects.create(user=self.user, action="Читать книгу", place="Гостиная", time_execution=120)
        # Публичная привычка
        self.public_habit = Habit.objects.create(
            user=self.user, action="Йога", place="Зал", time_execution=30, is_published=True
        )

        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_get_all_habits(self):
        """Тест получения списка своих привычек."""
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # Пагинация, поэтому 'results'
        self.assertEqual(data["results"][0]["action"], "Йога")

    def test_get_only_own_habits(self):
        """Тест, что видны только свои привычки."""
        response = self.client.get(reverse("habits:habits_list"))
        actions = [item["action"] for item in response.data["results"]]
        self.assertIn("Читать книгу", actions)
        self.assertNotIn("Бегать", actions)  # Привычка другого пользователя

    def test_create_habit(self):
        """Тест создания привычки."""
        url = reverse("habits:habit_create")
        data = {"action": "Писать код", "place": "Кабинет", "time_execution": 90, "periodicity": 1}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(response.data["action"], "Писать код")
        # Проверяем, что пользователь автоматически назначен
        self.assertEqual(Habit.objects.last().user, self.user)

    def test_get_single_habit(self):
        """Тест получения конкретной привычки."""
        response = self.client.get(reverse("habits:habit_retrieve", kwargs={"pk": self.habit.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["action"], "Читать книгу")

    def test_update_habit(self):
        """Тест обновления привычки."""
        url = reverse("habits:habit_update", kwargs={"pk": self.habit.pk})
        data = {"action": "Читать книгу", "place": "Кабинет", "time_execution": 120, "periodicity": 1}
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["place"], "Кабинет")

    def test_delete_habit(self):
        """Тест удаления привычки."""
        response = self.client.delete(reverse("habits:habit_delete", kwargs={"pk": self.habit.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 1)

    def test_get_public_habits(self):
        """Тест получения публичных привычек."""
        response = self.client.get(reverse("habits:public"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Йога")

    def test_public_habits_show_only_published(self):
        """Тест, что показываются только публичные привычки."""
        # Создаем еще одну НЕпубличную привычку
        Habit.objects.create(user=self.user, action="Секретная привычка", time_execution=60, is_published=False)

        response = self.client.get(reverse("habits:public"))

        # Должна быть только одна публичная
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Йога")

    def test_create_habit_with_both_related_and_award(self):
        """Тест: нельзя одновременно указывать связанную привычку и вознаграждение."""
        # Создаем приятную привычку для связи
        pleasant_habit = Habit.objects.create(
            user=self.user, action="Приятная привычка", pleasant_habit=True, time_execution=60
        )

        data = {
            "action": "Тест",
            "related_habit": pleasant_habit.id,
            "award": "Награда",  # Оба поля заполнены - ошибка
            "time_execution": 120,
        }

        response = self.client.post(
            reverse("habits:habit_create"), data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_create_habit_time_execution_too_long(self):
        """Тест: время выполнения не должно превышать 120 секунд."""
        data = {"action": "Тест", "time_execution": 130, "award": "Награда"}  # Больше 120 - ошибка

        response = self.client.post(
            reverse("habits:habit_create"), data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("time_execution", response.data)
