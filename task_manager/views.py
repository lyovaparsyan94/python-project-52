from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse
import rollbar

def test_rollbar(request):
    """Тест Rollbar на Render"""
    rollbar.report_message('✅ Render + Rollbar работает!', 'info')
    
    try:
        1 / 0
    except Exception:
        rollbar.report_exc_info()
    
    return HttpResponse('✅ Проверь Rollbar Dashboard через 30 сек!')

class IndexView(TemplateView):
    template_name = 'task_manager/index.html'

class BaseLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, 'Вы залогинены')
        return reverse_lazy('index')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин/пароль')
        return super().form_invalid(form)


def logout_view(request):
    """Простой logout GET"""
    logout(request)
    messages.success(request, 'Вы разлогинены')
    return redirect('index')