from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        self.existing_user = User.objects.create_user(
            username='existing',
            password='testpass123'
        )

    # CREATE TESTS
    def test_user_registration(self):
        # успешная регистрация
        url = reverse('users:create')
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_invalid_data(self):
        # регистрация с некорректными данными
        url = reverse('users:create')
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'mismatch'
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        password2_errors = response.context['form'].errors['password2']
        self.assertTrue(
            any("пароли не совпадают" in error for error in password2_errors))

    # UPDATE TESTS
    def test_update_user(self):
        # успешное обновление
        self.client.force_login(self.existing_user)
        url = reverse('users:update', kwargs={'pk': self.existing_user.pk})
        update_data = {
            'username': self.existing_user.username,
            'first_name': 'Updated',
            'last_name': 'Name',
            'password1': self.existing_user.password,
            'password2': self.existing_user.password,
        }
        response = self.client.post(url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.first_name, 'Updated')

    def test_update_unauthorized(self):
        # обновление без авторизации
        url = reverse('users:update', kwargs={'pk': self.existing_user.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login'))

    def test_update_other_user(self):
        # обновление чужого аккаунта
        another_user = User.objects.create_user(
            username='other', password='test123')
        self.client.force_login(self.existing_user)
        url = reverse('users:update', kwargs={'pk': another_user.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('users:list'))
        self.assertEqual(len(response.wsgi_request._messages), 1)

    # DELETE TESTS
    def test_delete_user(self):
        # успешное удаление
        self.client.force_login(self.existing_user)
        url = reverse('users:delete', kwargs={'pk': self.existing_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(
            pk=self.existing_user.pk).exists())

    def test_delete_unauthorized(self):
        # удаление без авторизации
        url = reverse('users:delete', kwargs={'pk': self.existing_user.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login'))

    def test_delete_other_user(self):
        # удаление чужого аккаунта
        another_user = User.objects.create_user(
            username='other', password='test123')
        self.client.force_login(self.existing_user)
        url = reverse('users:delete', kwargs={'pk': another_user.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users:list'))
        self.assertTrue(User.objects.filter(pk=another_user.pk).exists())
