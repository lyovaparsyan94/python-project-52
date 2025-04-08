from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages import info
from django.utils.translation import gettext, activate, get_language
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

class IndexView(TemplateView):
    template_name = "index.html"


class Login(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = gettext("You are log in")

    def form_valid(self, form):
        language = self.request.LANGUAGE_CODE
        activate(language)

        messages.success(self.request, self.success_message)

        return super().form_valid(form)


class Logout(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        info(request, gettext("You are log out"))
        return res
