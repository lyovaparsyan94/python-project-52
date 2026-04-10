from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied 
from .forms import CustomUserCreationForm, CustomUserUpdateForm



class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

class UserCreateView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('/login/')
        return render(request, 'users/create.html', {'form': form})
 
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users')
 
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения")
        return obj

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users')

    def delete(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(request, 'Вы не можете удалить другого пользователя')
            return redirect('users:users')
        
        messages.success(self.request, 'Пользователь успешно удален')
        return super(UserDeleteView, self).delete(request, *args, **kwargs)