from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAPITestCase(APITestCase):
    """Тесты для API пользователей."""
    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='existing_user',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_login_success(self):
        """Тест успешного входа пользователя."""
        url = reverse('users:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(url, data)
        print(f"Login success status: {response.status_code}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        """Тест входа с неправильным паролем."""
        url = reverse('users:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_registration_success(self):
        """Тест успешной регистрации нового пользователя."""
        url = reverse('users:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }

        response = self.client.post(url, data)
        print(f"Status: {response.status_code}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_token_refresh(self):
        """Тест обновления токена."""
        # Сначала получаем токен
        login_url = reverse('users:login')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        login_response = self.client.post(login_url, login_data)
        refresh_token = login_response.data.get('refresh')

        # Обновляем токен
        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_delete(self):
        """Тест удаления пользователя."""
        # Создаем отдельного пользователя для теста удаления
        delete_user = User.objects.create(
            email='deleteuser@example.com',
            username='deleteuser'
        )
        delete_user.set_password('testpass123')
        delete_user.save()

        # Аутентифицируем этого пользователя
        self.client.force_authenticate(user=delete_user)
        # Удаляем пользователя

    def test_user_password_is_hashed(self):
        """Пароль пользователя хэшируется."""
        user = User.objects.create(
            email='hash@example.com',
            username='hashuser'
        )
        raw_password = 'rawpassword123'
        user.set_password(raw_password)
        user.save()

        # Проверяем, что пароль не хранится в открытом виде
        self.assertNotEqual(user.password, raw_password)

        # Но проверка работает
        self.assertTrue(user.check_password(raw_password))
        self.assertFalse(user.check_password('wrongpassword'))
