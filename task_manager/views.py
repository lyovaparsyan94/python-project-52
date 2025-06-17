from django.views import View
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from django.http import HttpResponse

users = get_user_model()


def rollbar_test(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the pollapp index.")


class IndexView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'index.html'
        return render(request, template_name)


class TaskManagerLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class TaskManagerLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
