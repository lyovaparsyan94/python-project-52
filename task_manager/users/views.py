from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import LoginRequiredMixin, SelfAccessOnlyMixin
from task_manager.users.forms import (
    UserChangeForm,
    UserCreationForm,
)

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    ordering = ["id"]
    extra_context = {
        "title": _("Users"),
        "username": _("Username"),
        "full_name": _("Full name"),
        "created_at": _("Creation date"),
        "edit": _("Edit"),
        "delete": _("Delete"),
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    success_message = _("User was registered successfully")
    extra_context = {"title": _("Registration"), "button_name": _("Register")}


class UserUpdateView(
    LoginRequiredMixin,
    SelfAccessOnlyMixin,
    SuccessMessageMixin,
    UpdateView,
):
    permission_denied_url = reverse_lazy("users_list")
    permission_denied_message = _(
        "You don't have rights to change another user"
    )
    form_class = UserChangeForm
    model = User
    template_name = "form.html"
    success_url = reverse_lazy("users_list")
    success_message = _("User was updated successfully")
    extra_context = {
        "button_name": _("Update"),
        "title": _("Update user"),
    }


class UserDeleteView(
    LoginRequiredMixin,
    SelfAccessOnlyMixin,
    SuccessMessageMixin,
    DeleteView,
):
    permission_denied_url = reverse_lazy("users_list")
    permission_denied_message = _(
        "You don't have rights to delete another user"
    )
    template_name = "delete.html"
    model = User
    success_url = reverse_lazy("users_list")
    success_message = _("User was deleted successfully")
    extra_context = {
        "title": _("Delete user"),
        "button_name": _("Yes, delete"),
        "question": _("Are you sure you want to delete"),
    }
