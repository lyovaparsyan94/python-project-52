from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import UserCreateForm, UserLoginForm
from .models import User


class UserOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    error_message_auth = 'Вы не авторизованы! Пожалуйста, выполните вход.'
    error_message_permission = (
        'У вас нет прав для изменения другого пользователя.')
    error_message_relate = (
        'Невозможно удалить пользователя, потому что он используется')

    def test_func(self):
        user = self.get_object()

        return self.request.user == user and not (
            user.tasks_created.exists() or
            user.tasks_assigned.exists()
        )

    def handle_no_permission(self):
        user = self.get_object()

        if not self.request.user.is_authenticated:
            messages.error(self.request, self.error_message_auth)
            return redirect('login')

        if self.request.user != user:
            messages.error(self.request, self.error_message_permission)
            return redirect('users:list')

        if user.tasks_created.exists() or user.tasks_assigned.exists():
            messages.error(self.request, self.error_message_relate)
            return redirect('users:list')


class HomePageView(TemplateView):
    template_name = 'home.html'


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Вы залогинены'


class UserLogoutView(LogoutView):

    def dispatch(self, request):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request)


class UserUpdateView(UserOwnerMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(UserOwnerMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно удален'
