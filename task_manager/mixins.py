from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext
from django.urls import reverse_lazy


class AuthRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = gettext("Fast log in young bad boy")
        self.permission_denied_url = reverse_lazy("login")
        return super().dispatch(request, *args, **kwargs)
