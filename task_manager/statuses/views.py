from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from .forms import StatusForm
from .models import Status


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/index.html',
            {'statuses': statuses}
        )
        

class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        form = StatusForm()
        return render(
            request,
            'statuses/create.html',
            {'form': form}
        )
    
    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Статус успешно создан')
            return redirect(reverse('all_statuses'))
        return render(
            request,
            'statuses/create.html',
            {'form': form}
        )
    
    
class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        form = StatusForm(instance=status)
        return render(
            request,
            'statuses/update.html',
            {'form': form,
             'status_id': status_id},
        )
        
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = Status.objects.get(id=status_id)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Статус успешно изменен')
            return redirect(reverse('all_statuses'))
        return render(
            request, "statuses/update.html", {"form": form,
                                              "status_id": status_id}
        )
        
    
class StatusDeleteView(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        return render(
            request,
            'statuses/delete.html',
            {'status': status}
        )
        
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = Status.objects.get(id=status_id)
        if status.task_status.all():
            messages.add_message(request,
                                 messages.ERROR,
                    'Невозможно удалить статус, потому что он используется')
            return redirect(reverse('all_statuses'))
        status.delete()
        messages.add_message(request,
                                 messages.SUCCESS,
                                 'Статус успешно удален')
        return redirect(reverse('all_statuses'))