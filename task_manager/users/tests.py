from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.middleware.csrf import get_token
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UsersTest(TestCase):

    def test_users_list(self):
        response = self.client.get(reverse("usrs"))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name='Doe',
            username="piggiboy",
            password='111'
        )
        self.client.force_login(self.user)

    def test_user_create_flow(self):
        list_url = reverse("usrs")
        response = self.client.get(list_url)
        self.assertContains(response, "John")
        self.assertContains(response, "Doe")
        self.assertContains(response, "piggiboy")


class UserUpdateTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='piggiboy',
            password='testpass123',
            first_name='John',
            last_name='Doe',
        )

        self.update_url = reverse('update_user', kwargs={'pk': self.user.pk})
        self.login_url = reverse('login')

    def test_authenticated_user_can_update_self(self):
        self.client.force_login(self.user)

        get_response = self.client.get(self.update_url)
        csrf_token = get_token(get_response.wsgi_request)

        response = self.client.post(
            self.update_url,
            {
                'username': 'pigger',
                'first_name': 'John',
                'last_name': 'Doe',
                'password1': 111,
                'password2': 111,
                'csrfmiddlewaretoken': csrf_token,
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User successfully updated'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), _('User successfully updated'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'pigger')

    def test_unauthenticated_access_denied(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_update_others(self):
        other_user = get_user_model().objects.create_user(
            username='other',
            password='otherpass'
        )
        self.client.force_login(other_user)

        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(str(messages[0]), _(
            'You do not have permission to edit other users'))


class UserDeleteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.delete_url = reverse('delete_user', kwargs={'pk': self.user.pk})


    def test_authenticated_user_can_delete_self(self):
        self.client.force_login(self.user)

        delete_url = reverse('delete_user', kwargs={'pk': self.user.pk})

        response = self.client.post(delete_url, follow=True)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        messages_list = [str(m) for m in response.context['messages']]
        self.assertIn(_('User succesfully deleted'), messages_list)

    def test_unauthenticated_user_cannot_delete(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_cannot_delete_other_user(self):
        other_user = User.objects.create_user(first_name="John",
                                              last_name='Doughmaker',
                                              username="Mr",
                                              password='111')
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('delete_user', kwargs={'pk': other_user.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
