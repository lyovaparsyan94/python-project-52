from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from ..mixins import AuthRequiredMessageMixin
from .consts import TasksConst
from .forms import (LabelForm, LabelFormDelete, StatusForm, StatusFormDelete,
                    TaskForm, TaskFormDelete)
from .models import Label, Status, Task
from .filters import TaskFilter


class SimpleIndexView(AuthRequiredMessageMixin, View):

    model = None
    term = ''
    terms = ''
    term_url = ''
    term_update_url = ''
    term_delete_url = ''
    page_url = 'tasks/index_simple.html' 

    def get(self, request, *args, **kwargs):
        items = list(self.model.objects.all())
        return render(
            request,
            self.page_url,
            context={
                'items': items,
                'term': self.term,
                'terms': self.terms,
                'term_url': self.term_url,
                'term_update_url': self.term_update_url,
                'term_delete_url': self.term_delete_url,
            },
        )


class StatusIndexView(SimpleIndexView):
    model = Status
    term = TasksConst.status_term
    terms = TasksConst.status_terms
    term_url = 'tasks:create_status'
    term_update_url = 'tasks:update_status'
    term_delete_url = 'tasks:delete_status'


class LabelIndexView(SimpleIndexView):
    model = Label
    term = TasksConst.label_term
    terms = TasksConst.labels_terms
    term_url = 'tasks:create_label'
    term_update_url = 'tasks:update_label'
    term_delete_url = 'tasks:delete_label'


class SimpleFormCreateView(AuthRequiredMessageMixin, View):

    form = None
    form_title = ''
    btn_title = ''
    succ_mess = ''
    list_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, self.succ_mess)
            return redirect(self.list_url)

        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })


class StatusFormCreateView(SimpleFormCreateView):
    form = StatusForm
    form_title = TasksConst.status_create_title
    btn_title = TasksConst.create_btn_title
    succ_mess = TasksConst.status_succ_create
    list_url = 'tasks:status_list'


class LabelFormCreateView(SimpleFormCreateView):
    form = LabelForm
    form_title = TasksConst.label_create_title
    btn_title = TasksConst.create_btn_title
    succ_mess = TasksConst.label_succ_create
    list_url = 'tasks:label_list'


class SimpleFormUpdateView(AuthRequiredMessageMixin, View):
    model = None
    form = None
    form_title = ''
    btn_title = ''
    succ_mess = ''
    list_url = ''

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        
        item = get_object_or_404(self.model, id=id)
        form = self.form(instance=item)
        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        item = get_object_or_404(self.model, id=id)
        form = self.form(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(self.request, self.succ_mess)
            return redirect(self.list_url)

        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })


class StatusFormUpdateView(SimpleFormUpdateView):
    model = Status
    form = StatusForm
    form_title = TasksConst.status_update_title
    btn_title = TasksConst.update_btn_title
    succ_mess = TasksConst.status_succ_update
    list_url = 'tasks:status_list'


class LabelFormUpdateView(SimpleFormUpdateView):
    model = Label
    form = LabelForm
    form_title = TasksConst.label_update_title
    btn_title = TasksConst.update_btn_title
    succ_mess = TasksConst.label_succ_update
    list_url = 'tasks:label_list'


class SimpleFormDeleteView(AuthRequiredMessageMixin, View):
    model = None
    form = None
    form_title = ''
    succ_mess = ''
    err_mess = ''
    list_url = ''
    not_owner_mess = ''
    is_owner_only = False

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        item = get_object_or_404(self.model, id=id)
        form = self.form(instance=item)
        return render(
            request,
            'tasks/delete_simple.html',
            {
                'form': form,
                'item': item,
                'form_title': self.form_title
            })

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        item = get_object_or_404(self.model, id=id)
        
        if self.is_owner_only and item.author != request.user:
            messages.error(self.request, self.not_owner_mess)
            return redirect(reverse('tasks:task_list')) 

        if item:
            try:
                item.delete()
                messages.success(self.request, self.succ_mess)

            except ProtectedError:
                messages.error(self.request, self.err_mess)
        return redirect(self.list_url)


class StatusFormDeleteView(SimpleFormDeleteView):
    model = Status
    form = StatusFormDelete
    form_title = TasksConst.status_delete_title
    succ_mess = TasksConst.status_succ_delete
    err_mess = TasksConst.status_used
    list_url = 'tasks:status_list'


class LabelFormDeleteView(SimpleFormDeleteView):
    model = Label
    form = LabelFormDelete
    form_title = TasksConst.delete_label_title
    succ_mess = TasksConst.label_succ_delete
    err_mess = TasksConst.label_used
    list_url = 'tasks:label_list'


class TaskFormCreateView(SimpleFormCreateView):
    form = TaskForm
    form_title = TasksConst.task_create_title
    btn_title = TasksConst.create_btn_title
    succ_mess = TasksConst.task_succ_create
    list_url = 'tasks:task_list'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            task_obj = form.save(commit=False)
            task_obj.author_id = request.user.id
            task_obj.save()
            task_obj.labels.set(form.cleaned_data['labels'])
            form.save_m2m()
            messages.success(self.request, self.succ_mess)
            return redirect(self.list_url)
        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })


class TaskFormUpdateView(SimpleFormUpdateView):
    model = Task
    form = TaskForm
    form_title = TasksConst.task_update_title
    btn_title = TasksConst.update_btn_title
    succ_mess = TasksConst.task_succ_update
    list_url = 'tasks:task_list'

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        item = get_object_or_404(self.model, id=id)
        form = self.form(request.POST, instance=item)
        if form.is_valid():
            task_obj = form.save(commit=False)
            task_obj.author_id = request.user.id
            task_obj.save()
            task_obj.labels.set(form.cleaned_data['labels'])
            form.save_m2m()
            messages.success(self.request, self.succ_mess)
            return redirect(self.list_url)

        return render(
            request,
            'tasks/create_simple.html',
            {
                'form': form,
                'form_title': self.form_title,
                'btn_title': self.btn_title
            })


class TaskFormDeleteView(SimpleFormDeleteView):
    model = Task
    form = TaskFormDelete
    form_title = TasksConst.task_delete_title
    succ_mess = TasksConst.task_succ_delete
    list_url = 'tasks:task_list'
    is_owner_only = True
    not_owner_mess = TasksConst.task_error_delete


class TaskIndexView(SimpleIndexView):
    model = Task
    term = TasksConst.task_term
    terms = TasksConst.tasks_terms
    term_url = 'tasks:create_task'
    term_update_url = 'tasks:update_task'
    term_delete_url = 'tasks:delete_task'
    page_url = 'tasks/index_tasks.html'

    def get(self, request, *args, **kwargs):

        queryset = self.model.objects.all()
        filter = TaskFilter(request.GET, queryset=queryset, request=request)
        filtered_queryset = filter.qs
        return render(
            request,
            self.page_url,
            context={
                'filter': filter,
                'items': filtered_queryset,
                'term': self.term,
                'terms': self.terms,
                'term_url': self.term_url,
                'term_update_url': self.term_update_url,
                'term_delete_url': self.term_delete_url,
            },
        )


class TaskView(AuthRequiredMessageMixin, View):

    model = Task
    update_url = 'tasks:update_task'
    delete_url = 'tasks:delete_task'
    page_url = 'tasks/task_card.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')

        item = get_object_or_404(self.model, id=id)
        return render(
            request,
            self.page_url,
            {
                'item': item,
                'labels': item.labels.all(),
                'update_url': self.update_url,
                'delete_url': self.delete_url
            })
