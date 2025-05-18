from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        messages.error(self.request, _("You don't have permission to change another user."))
        return redirect("users:list")
