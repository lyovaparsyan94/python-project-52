from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .forms import UserLoginForm
from .mixins import ContextMixin, FormValidMixin


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(ContextMixin, FormValidMixin, LoginView):
    authentication_form = UserLoginForm
    success_url = reverse_lazy("index")
    text = _("Login")
    button = _("Log in")
    redirect_authenticated_user = True
    template_name = "general_form.html"
    success_message = _("You are logged in")
    error_message = _(
        "Please enter the correct username and password. "
        "Both fields can be case-sensitive."
    )


class LogoutView(BaseLogoutView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        super().post(request, *args, **kwargs)
        return redirect("/")