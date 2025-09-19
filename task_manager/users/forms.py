from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_user_model_lazy():
    from django.contrib.auth import get_user_model
    return get_user_model()


class RegistrationUserForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'minlength': '3',
            'required': 'required',
        }),
        help_text=_('Your password must contain at least 3 characters.'),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
        help_text=_('Enter the same password as before, for verification.'),
    )

    class Meta:
        model = get_user_model_lazy()
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2']
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': _('First name'),
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': _('Last name'),
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': _('Username'),
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': _("The two password fields didn't match.")
            })

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model_lazy()

        if not username:
            return username

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                _('A user with that username already exists.'))

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
        return user


class UpdateUserForm(RegistrationUserForm):
    pass
