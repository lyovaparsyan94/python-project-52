from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    '''creates a user authorization form'''

    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Username')
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })
