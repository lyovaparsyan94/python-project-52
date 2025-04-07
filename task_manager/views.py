from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import info


class IndexView(TemplateView):
    template_name = 'index.html'


class Login(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = gettext('You are log in')


class Logout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        info(request, gettext('You are log out'))
        return res