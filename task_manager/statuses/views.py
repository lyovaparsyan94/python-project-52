from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.models import Tasks

from .forms import CreateStatusesForm
from .models import Statuses


class BaseStatusView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'))
        return super().dispatch(request, *args, **kwargs)
    

class IndexStatusesView(BaseStatusView):
    def get(self, request):
        statuses = Statuses.objects.all().order_by('id')
        return render(
            request,
            'statuses/index.html',
            context={
                'statuses': statuses
            }
        )


class CreateStatusesView(BaseStatusView):
    def get(self, request):
        return self._render_form(request, CreateStatusesForm())

    def post(self, request):
        form = CreateStatusesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect('statuses')
        return self._render_form(request, form)

    def _render_form(self, request, form):
        return render(
            request,
            'statuses/create.html',
            context={
                'form': form
            }
        )

        
class UpdateStatusesView(BaseStatusView):
    def get(self, request, pk):
        status = get_object_or_404(Statuses, pk=pk)
        return self._render_form(
            request, CreateStatusesForm(instance=status), status
        )

    def post(self, request, pk):
        status = get_object_or_404(Statuses, pk=pk)
        form = CreateStatusesForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully updated'))
            return redirect('statuses')
        return self._render_form(request, form, status)

    def _render_form(self, request, form, status):
        return render(
            request,
            'statuses/update.html',
            context={
                'form': form,
                'status': status,
            }
        )


class DeleteStatusesView(BaseStatusView):
    def get(self, request, pk):
        status = Statuses.objects.get(pk=pk)
        return render(
            request,
            'statuses/delete.html',
            context={
                'status': status,
            }
        )

    def post(self, request, pk):
        status = get_object_or_404(Statuses, pk=pk)
        if Tasks.objects.filter(status=status).exists():
            messages.error(
                request,
                _('Cannot delete status because it is in use')
            )
            return redirect('statuses')
        status.delete()
        messages.success(request, _('Status successfully deleted'))
        return redirect('statuses')
