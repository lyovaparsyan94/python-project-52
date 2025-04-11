from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import LoginRequiredMixin, ProtectErrorMixin
from task_manager.statuses.forms import StatusCreationForm
from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"
    ordering = ["id"]
    extra_context = {"title": _("Statuses"), "create": _("Create status")}


class StatusCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Status
    template_name = "form.html"
    form_class = StatusCreationForm
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status was created successfully")
    extra_context = {"title": _("Create status"), "button_name": _("Create")}


class StatusUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    form_class = StatusCreationForm
    model = Status
    template_name = "form.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status was updated successfully")
    extra_context = {
        "title": _("Update status"),
        "button_name": _("Update"),
    }


class StatusDeleteView(
    LoginRequiredMixin,
    ProtectErrorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = Status
    success_url = reverse_lazy("statuses_list")
    success_message = _("Status was deleted successfully")
    protected_object_url = reverse_lazy("statuses_list")
    protected_object_message = _(
        "Cannot delete this status because it is being used"
    )
    extra_context = {
        "title": _("Delete status"),
        "button_name": _("Yes, delete"),
        "question": _("Are you sure you want to delete"),
    }
