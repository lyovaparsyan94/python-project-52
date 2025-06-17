from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AuthRequiredMessageMixin(LoginRequiredMixin):
    you_are_not = 'Вы не авторизованы! Пожалуйста, выполните вход.'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.you_are_not)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class IsOwnerMixin(UserPassesTestMixin):
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав \
                       для изменения другого пользователя.')
        return redirect(reverse_lazy('users:users')) 

    def test_func(self):
        target_user = self.get_object()
        return self.request.user == target_user
