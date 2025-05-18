from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect

from .models import User
from .forms import UserForm
from .mixins import UserPermissionMixin


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")


class UserUpdateView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully updated")


class UserDeleteView(LoginRequiredMixin, UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User successfully deleted")

    def delete(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(request, _("Cannot delete user because it is used"))
            return redirect("users:list")
        return super().delete(request, *args, **kwargs)
