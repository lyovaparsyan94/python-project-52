from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно создана")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно изменена")


class LabelDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно удалена")

    def test_func(self):
        return self.request.user == self.get_object().creator

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(request, _("Невозможно удалить метку," 
            " используемую в задачах"))
            return redirect('labels_list')
        return super().post(request, *args, **kwargs)