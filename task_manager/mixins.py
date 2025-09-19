from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class MessageMixin:
    '''outputs custom messages about successful and unsuccessful operations'''
    success_message = _('Operation completed successfully.')
    error_message = _('An error occurred.')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)
