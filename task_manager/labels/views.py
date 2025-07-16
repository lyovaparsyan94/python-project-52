from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.models import Task

from .forms import CreateLabelsForm
from .models import Label


class BaseLabelsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'))
        return super().dispatch(request, *args, **kwargs)


class IndexLabelsView(BaseLabelsView):
    def get(self, request):
        labels = Label.objects.all().order_by('id')
        return render(
            request,
            'labels/index.html',
            context={
                'labels': labels
            },
        )


class CreateLabelsView(BaseLabelsView):
    def get(self, request):
        return self._render_form(request, CreateLabelsForm())

    def post(self, request):
        form = CreateLabelsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully created'))
            return redirect('labels')
        return self._render_form(request, form)
    
    def _render_form(self, request, form):
        return render(
            request,
            'labels/create.html',
            context={
                'form': form
            }
        )


class UpdateLabelsView(BaseLabelsView):
    def get(self, request, pk):
        labels = get_object_or_404(Label, pk=pk)
        form = CreateLabelsForm(instance=labels)
        return render(
            request,
            'labels/update.html',
            context={
                'form': form,
                'labels': labels
            }
        )

    def post(self, request, pk):
        labels = get_object_or_404(Label, pk=pk)
        form = CreateLabelsForm(request.POST, instance=labels)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully updated'))
            return redirect('labels')
        return render(
            request,
            'labels/update.html',
            context={
                'form': form,
                'labels': labels
            }
        )


class DeleteLabelsView(BaseLabelsView):
    def get(self, request, pk):
        labels = get_object_or_404(Label, pk=pk)
        return render(
            request,
            'labels/delete.html',
            context={
                'labels': labels
            }
        )
    
    def post(self, request, pk):
        labels = get_object_or_404(Label, pk=pk)
        if Task.objects.filter(labels=labels).exists():
            messages.error(
                request, 
                _('Cannot delete label because it is in use')
            )
            return redirect('labels')
        labels.delete()
        messages.success(request, _('Label successfully deleted'))
        return redirect('labels')