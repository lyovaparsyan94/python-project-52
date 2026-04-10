from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from task_manager.models import Status
from django.shortcuts import redirect


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/update.html'

    def get_success_url(self):
        return reverse_lazy('statuses:statuses')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:statuses')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.task_set.exists():
            messages.error(request, 'Невозможно удалить статус')
            return redirect('statuses:statuses')

        messages.success(self.request, 'Статус успешно удален')
        return super().delete(request, *args, **kwargs)