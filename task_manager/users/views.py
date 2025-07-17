from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from .forms import UserRegForm, UserUpdateForm
from .models import User


# Create your views here.
class IndexUserView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.order_by('id').all()
        return render(
            request,
            'users/index.html',
            {'users': users}
        )
    
    
class UserRegister(View):
    def post(self, request, *args, **kwargs):
        form = UserRegForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Пользователь успешно зарегистрирован')
            return redirect(reverse('login'))
        return render(request, 'users/create.html', {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = UserRegForm()
        return render(
            request,
            'users/create.html',
            {'form': form}
        )
        

class UserUpdate(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if request.user.id == kwargs.get('id'):
            form = UserUpdateForm(initial={
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })
            return render(
                request,
                'users/update.html',
                {'form': form,
                 'id': request.user.id
                }
            )
        messages.add_message(request,
                             messages.ERROR,
                        'У вас нет прав для изменения другого пользователя.')
        return redirect(reverse('all_users'))
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserUpdateForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Пользователь успешно изменен')
            return redirect(reverse('all_users'))
        return render(
            request,
            'users/update.html',
            {'form': form}
        )
        
    
class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                        'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if request.user.id == kwargs.get('id'):
            return render(
                request,
                'users/delete.html',
            )
        messages.add_message(request,
                             messages.ERROR,
                        'У вас нет прав для изменения другого пользователя.')
        return redirect(reverse('all_users'))
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user.task_creator.all():
            messages.add_message(request,
                             messages.ERROR,
            'Пользователь используется и не может быть удален')
            return redirect(reverse('all_users'))
        user.delete()
        messages.add_message(request,
                                messages.SUCCESS,
                                'Пользователь успешно удален')
        return redirect(reverse('all_users'))