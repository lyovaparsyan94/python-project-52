from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    ContextDeleteMixin,
    ContextMixin,
    UserDeletePermissionMixin,
    UserEditPermissionMixin,
)

from .forms import UserRegisterForm
from .models import User


class UsersIndexView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"


class UsersCreateView(ContextMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    text = _("Registration")
    button = _("Register")
    success_message = _("The user has been successfully registered")


class UsersUpdateView(UserEditPermissionMixin, ContextMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users")
    text = _("Changing the user")
    button = _("Change")
    success_message = _("User successfully edited")
    error_message = _("Please correct the errors below.")


class UserDeleteView(
    UserDeletePermissionMixin,
    ContextDeleteMixin,
    DeleteView
):
    model = User
    success_url = reverse_lazy("users")
    text = _("Deleting user")
    success_delete_message = _("User successfully deleted")
    display_attribute = 'username'
