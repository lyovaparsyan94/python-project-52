from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class FormStyleMixin:
    """Adds Bootstrap styles to form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_input_class = (
            'form-control bg-secondary bg-opacity-50 border-secondary'
        )
        base_select_class = (
            'form-select bg-secondary bg-opacity-50 border-secondary'
        )

        for name, field in self.fields.items():
            attrs = {
                'placeholder': field.label
            }

            if name == 'description':
                attrs['class'] = base_input_class
                attrs['rows'] = '3'
            elif name in ['status', 'executor']:
                attrs['class'] = base_select_class
            else:
                attrs['class'] = base_input_class

            field.widget.attrs.update(attrs)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin that requires the user to be authenticated.

    If the user is not authenticated, shows an error message
    and redirects them to the login page without using the default
    'next' query parameter.
    """
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def handle_no_permission(self):
        """
        Adds an error message if the user is not authenticated
        and delegates to the default permission handler.

        Returns:
            HttpResponse: A redirect to the login page or another
            appropriate response from the base class.
        """
        if not self.request.user.is_authenticated:
            msg = _('You are not authorized! Please, log in.')
            messages.error(self.request, msg)
        return super().handle_no_permission()


class BasePermissionMixin(UserPassesTestMixin):
    """Base mixin for object permission checks."""
    permission_denied_url = reverse_lazy('users:index')
    permission_denied_message = _('Permission denied')
    redirect_field_name = None

    def handle_no_permission(self):
        """
        Redirects authenticated users with error message, or defers to parent.

        Returns:
            HttpResponse: Redirect or default permission handling.
        """
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)
        return super().handle_no_permission()


class UserPermissionMixin(BasePermissionMixin):
    """Allows access only to the profile owner."""
    msg = _('You do not have permission to change another user.')
    permission_denied_message = msg

    def test_func(self):
        """
        Checks if the requesting user matches the object user.

        Returns:
            bool: True if user is owner, else False.
        """
        return self.get_object() == self.request.user


class AuthorPermissionMixin(BasePermissionMixin):
    """Allows access only to the object author."""
    msg = _('You do not have permission to change this object.')
    permission_denied_message = msg

    def test_func(self):
        """
        Checks if the requesting user is the object's author.

        Returns:
            bool: True if user is author, else False.
        """
        return self.get_object().author == self.request.user


class ProtectErrorMixin:
    """Handles ProtectedError exceptions on object deletion."""
    protected_object_message = _(
        'Cannot delete object because it is being used.'
    )
    protected_object_url = None

    def post(self, request, *args, **kwargs):
        """
        Attempts to delete object and handles ProtectedError.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Redirects with error message if deletion fails.
        """
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_object_message)
            return redirect(self.protected_object_url)
