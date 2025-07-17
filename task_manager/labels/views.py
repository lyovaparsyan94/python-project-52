from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.models import Tasks

from .forms import CreateLabelsForm
from .models import Labels


class BaseLabelsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'))
        return super().dispatch(request, *args, **kwargs)
    

class IndexLabelsView(BaseLabelsView):
    def get(self, request):
        labels = Labels.objects.all()
        return render(
            request, 
            'labels/index.html', 
            context={
                'labels': labels
            }
        )
    

class CreateLabelsView(BaseLabelsView):
    def get(self, request):
        return self._render_form(request, CreateLabelsForm())

    def post(self, request):
        form = CreateLabelsForm(request.POST)
        if form.is_valid():
            form.save()
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
        label = get_object_or_404(Labels, pk=pk)
        return self._render_form(
            request, CreateLabelsForm(instance=label), label
        )

    def post(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        form = CreateLabelsForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully updated'))
            return redirect('labels')
        return self._render_form(request, form, label)

    def _render_form(self, request, form, label):
        return render(
            request,
            'labels/update.html',
            context={
                'form': form,
                'label': label,
            }
        )


class DeleteLabelsView(BaseLabelsView):
    def get(self, request, pk):
        label = Labels.objects.get(pk=pk)
        return render(
            request,
            'labels/delete.html',
            context={
                'label': label,
            }
        )

    def post(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        if Tasks.objects.filter(label=label).exists():
            messages.error(
                request,
                _('Cannot delete label because it is in use')
            )
            return redirect('labels')
        label.delete()
        messages.success(request, _('Label successfully deleted'))
        return redirect('labels')