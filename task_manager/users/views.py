from django.contrib import messages
from .models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from ..mixins import AuthRequiredMessageMixin, IsOwnerMixin
from .forms import TaskManagerUserCreateForm as UserCreateForm
from .forms import UpdateUser


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        template_name = 'users/index.html'
        return render(request, template_name, {'users': users})


class CreateUserView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return response


class UpdateUserView(AuthRequiredMessageMixin, IsOwnerMixin, UpdateView):
    model = User
    form_class = UpdateUser

    template_name = 'users/change.html'
    success_url = reverse_lazy('users:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно изменен')
        return response

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('id')
        return get_object_or_404(User, id=user_id)


class DeleteUserView(AuthRequiredMessageMixin, IsOwnerMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 
                           'Невозможно удалить пользователя, потому что он используется')
            return redirect(self.success_url)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно удален')
        return response

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('id')
        return get_object_or_404(User, id=user_id)
