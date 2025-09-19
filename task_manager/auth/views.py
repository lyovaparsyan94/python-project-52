from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from task_manager.mixins import MessageMixin

from .forms import LoginForm


class LoginView(MessageMixin, auth_views.LoginView):
    template_name = 'base_template/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_message = _('You are logged in')
    error_message = None

    def get_context_data(self, **kwargs):
        '''add form instance to template context.
        extends parent context with the form instance to ensure
        the template has access to the form object'''
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        '''determine redirect URL after successful form submission'''
        next_url = self.request.POST.get(
            'next') or self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


@method_decorator(csrf_protect, name='dispatch')
class LogoutView(auth_views.LogoutView):
    '''
    - enforces CSRF protection on dispatch
    - redirects to the 'home' page after logout
    - adds an informational message for the user after logout
    '''
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):

        messages.info(request, _('You have logged out'))
        return super().dispatch(request, *args, **kwargs)
