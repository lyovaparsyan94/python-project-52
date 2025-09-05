from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    ContextDeleteMixin,
    ContextMixin,
    CustomLoginRequiredMixin,
)

from .forms import LabelForm
from .models import Label


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(CustomLoginRequiredMixin, ContextMixin, CreateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("label_list")
    text = _("Create label")
    button = _("Create")
    success_message = _("Label created successfully")


class LabelUpdateView(CustomLoginRequiredMixin, ContextMixin, UpdateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("label_list")
    text = _("Update label")
    button = _("Update")
    success_message = _("Label updated successfully")


class LabelDeleteView(
    CustomLoginRequiredMixin,
    ContextDeleteMixin,
    DeleteView
):
    model = Label
    success_url = reverse_lazy("label_list")
    text = _("Delete label")
    success_delete_message = _("Label deleted successfully")