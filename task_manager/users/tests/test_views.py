from django.contrib.auth import get_user_model
from django.urls import reverse

from .testcase import UserTestCase

User = get_user_model()


class UserViewsTest(UserTestCase):
    def test_user_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(
            reverse('user_update', args=[self.user.pk]),
            self.update_data
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(
            reverse('user_delete', args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)
