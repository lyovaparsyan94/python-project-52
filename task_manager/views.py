from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from task_manager.users.forms import UserLoginForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'index.html',
        )
           
    
class LoginUser(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(
            request,
            'users/login.html',
            context={
                'form': form,
            },
        )
        
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Вы залогинены')
                return redirect(reverse('main_index'))
        return render(request, 'users/login.html', {'form': form})
    
    
class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('main_index'))

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Вы разлогинены')
        auth.logout(request)
        return redirect(reverse('main_index'))
