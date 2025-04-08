from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from task_manager.labels.models import Labels
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequired
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext
from django.contrib import messages


# Create your views here.


class LabelsListView(AuthRequired, ListView):
    template_name = "labels/list.html"
    model = Labels


class LabelsCreate(AuthRequired, SuccessMessageMixin, CreateView):
    template_name = "labels/create.html"
    model = Labels
    form_class = LabelForm
    success_url = reverse_lazy("labels:list")
    success_message = gettext("Label create")


class LabelsUpdate(AuthRequired, SuccessMessageMixin, UpdateView):
    template_name = "statuses/update.html"
    model = Labels
    form_class = LabelForm
    success_url = reverse_lazy("labels:list")
    success_message = gettext("Label update")


class LabelsDelete(AuthRequired, SuccessMessageMixin, DeleteView):
    template_name = "labels/delete.html"
    model = Labels
    success_url = reverse_lazy("labels:list")
    success_message = gettext("Label delete")

    def post(self, request, *args, **kwargs):
        if self.get_object().labels.all().exists():
            messages.error(self.request, gettext("label to delete unreal"))
            return redirect("labels:list")
        return super().post(request, *args, **kwargs)
