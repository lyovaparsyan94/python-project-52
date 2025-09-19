from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import MessageMixin
from task_manager.tasks.models import Tasks

from .forms import CreateStatusForm, UpdateStatusForm
from .models import Statuses


class StatusView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'status_template/statuses.html'
    context_object_name = 'statuses'
    login_url = '/login/'


class StatusUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Statuses
    template_name = 'status_template/status_update.html'
    context_object_name = 'update_status'
    login_url = '/login/'
    success_url = reverse_lazy('status')
    form_class = UpdateStatusForm
    success_message = _('Status updated successfully')
    error_message = _('Status with this Name already exists')

    def get_context_data(self, **kwargs):
        status = self.object
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Update")
        context['status_id'] = status.id
        context['title_text'] = _('Update status')
        return context


class StatusCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Statuses
    template_name = 'status_template/status_create.html'
    context_object_name = 'create_status'
    login_url = '/login/'
    form_class = CreateStatusForm
    success_url = reverse_lazy('status')
    success_message = _('Status created successfully')
    error_message = _('Status with this Name already exists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Create")
        context['title_text'] = _("Create status")
        return context


class StatusDelete(LoginRequiredMixin, DeleteView):
    model = Statuses
    template_name = 'status_template/status_delete.html'
    success_url = reverse_lazy('status')
    context_object_name = 'name'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if Tasks.objects.filter(status=self.object).exists():
            messages.error(
                request,
                _('Cannot delete status because it is in use')
            )
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            _('Status deleted successfully!')
        )
        return super().delete(request, *args, **kwargs)
