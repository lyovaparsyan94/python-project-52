from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from .forms import LabelForm
from .models import Label


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        labels = Label.objects.all()
        return render(
            request,
            'labels/index.html',
            {'labels': labels}
        )
        

class LabelCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        form = LabelForm()
        return render(
            request,
            'labels/create.html',
            {'form': form}
        )
    
    def post(self, request, *args, **kwargs):
        form = LabelForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Метка успешно создана')
            return redirect(reverse('all_labels'))
        return render(
            request,
            'labels/create.html',
            {'form': form}
        )
    
    
class LabelUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        form = LabelForm(instance=label)
        return render(
            request,
            'labels/update.html',
            {'form': form,
             'label_id': label_id},
        )
        
    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("id")
        label = Label.objects.get(id=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Метка успешно изменена')
            return redirect(reverse('all_labels'))
        return render(
            request, "labels/update.html", {"form": form,
                                              "label_id": label_id}
        )
        
    
class LabelDeleteView(View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        return render(
            request,
            'labels/delete.html',
            {'label': label}
        )
        
    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = Label.objects.get(id=label_id)
        if label.task_label.all():
            messages.add_message(request,
                                 messages.ERROR,
                    'Невозможно удалить метку, потому что она используется')
            return redirect(reverse('all_labels'))
        label.delete()
        messages.add_message(request,
                                 messages.SUCCESS,
                                 'Метка успешно удалена')
        return redirect(reverse('all_labels'))