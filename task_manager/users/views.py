from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.http import HttpResponseForbidden

from task_manager.mixins import MessageMixin

from task_manager.users.forms import RegistrationUserForm, UpdateUserForm


class UsersView(ListView):
    model = get_user_model()
    template_name = 'base_template/users.html'
    context_object_name = 'usrs'


class UserCreateView(MessageMixin, CreateView):
    model = get_user_model()
    form_class = RegistrationUserForm
    template_name = 'user_template/create.html'
    success_url = reverse_lazy('home')
    success_message = _('Registration successful!')
    error_message = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Create")
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     MessageMixin, UpdateView):
    model = get_user_model()
    form_class = UpdateUserForm
    template_name = 'user_template/update.html'
    success_url = reverse_lazy('usrs')
    success_message = _('User successfully updated')
    login_url = '/login/'
    error_message = None

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You do not have permission to edit other users'))
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Update")
        return context


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'user_template/delete.html'
    success_url = reverse_lazy('home')
    permission_denied_template = 'usrs'
    success_message = _('User successfully deleted')
    login_url = '/login/'

    def test_func(self):
        user_to_delete = self.get_object()
        return self.request.user == user_to_delete

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        user.delete()

        return redirect(self.success_url)

    def handle_no_permission(self):
        messages.error(
                self.request,
                _('You do not have permission to modify another user.')
            )
        return HttpResponseForbidden("Forbidden")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context
