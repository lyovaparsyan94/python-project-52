from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import Users


class CreateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label=_("Confirm Password"), 
        widget=forms.PasswordInput,
        help_text=_('To confirm, please enter your password again.')
    )

    class Meta:
        model = Users
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'confirm_password'
        ]
        help_texts = {
            'username': _("Required. 150 characters or fewer. "
                          "Letters, digits and @/./+/-/_ only."),
            'password': _("<ul><li>Your password must be at "
                          "least 3 characters long.</ul></li>")
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username'),
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError(
                _("You must enter a password.")
            )        
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                _("The passwords entered do not match.")
            )
        if len(password) < 3:
            raise forms.ValidationError(
                _("The password you entered is too short. "
                  "It must contain at least 3 characters.")
            )
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']   
        if len(username) > 150:
            raise forms.ValidationError(
                _("Username is too long (maximum 150 characters).")
            )        
        if not all(c.isalnum() or c in '@.+-_' for c in username):
            raise forms.ValidationError(
                _("Please enter a valid username. "
                  "It can only contain letters, numbers and @/./+/-/_ signs.")
            )
        
        User = get_user_model()
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            if not hasattr(self, 'instance') \
                or self.instance.pk != existing_user.pk:
                raise forms.ValidationError(
                    _("A user with this name already exists.")
                )
        return username

