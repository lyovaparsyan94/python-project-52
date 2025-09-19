from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import MessageMixin

from .forms import CreateLabelForm, UpdateLabelForm
from .models import Labels


class LabelsView(LoginRequiredMixin, ListView):
    model = Labels
    template_name = 'label_template/labels.html'
    context_object_name = 'labels'
    login_url = '/login/'


class LabelUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Labels
    template_name = 'label_template/label_update.html'
    context_object_name = 'update_label'
    login_url = '/login/'
    form_class = UpdateLabelForm
    success_url = reverse_lazy('labels')
    success_message = _('The label was successfully updated')
    error_message = _('Label with this Name already exists')

    def get_context_data(self, **kwargs):
        label = self.object
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Update")
        context['label_id'] = label.id
        context['title_text'] = _('Update label')
        return context


class LabelCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Labels
    template_name = 'label_template/label_create.html'
    context_object_name = 'create_label'
    login_url = '/login/'
    form_class = CreateLabelForm
    success_url = reverse_lazy('labels')
    success_message = _('The label was successfully created')
    error_message = _('Label with this Name already exists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_text'] = _("Create label")
        return context


class LabelDelete(LoginRequiredMixin, MessageMixin, DeleteView):
    model = Labels
    template_name = 'label_template/label_delete.html'
    context_object_name = 'del_label'
    login_url = '/login/'
    success_url = reverse_lazy('labels')
    success_message = _('The label was successfully deleted')
