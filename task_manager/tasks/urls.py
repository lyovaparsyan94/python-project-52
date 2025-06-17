from django.urls import path

from task_manager.tasks.views import (LabelFormCreateView, LabelFormDeleteView,
                                      LabelFormUpdateView, LabelIndexView,
                                      StatusFormCreateView,
                                      StatusFormDeleteView,
                                      StatusFormUpdateView, StatusIndexView,
                                      TaskFormCreateView, TaskFormUpdateView,
                                      TaskIndexView, TaskView, TaskFormDeleteView)

app_name = 'tasks'

urlpatterns = [
    path("statuses/", StatusIndexView.as_view(), name='status_list'),
    path("labels/", LabelIndexView.as_view(), name='label_list'),
    path(
        'statuses/create/',
        StatusFormCreateView.as_view(),
        name='create_status'
    ),
    path(
        'statuses/<int:pk>/update/',
        StatusFormUpdateView.as_view(),
        name='update_status'
    ),
    path(
        'statuses/<int:pk>/delete/',
        StatusFormDeleteView.as_view(),
        name='delete_status'
    ),

    path('labels/create/', LabelFormCreateView.as_view(), name='create_label'),
    path(
        'labels/<int:pk>/update/',
        LabelFormUpdateView.as_view(),
        name='update_label'
    ),
    path(
        'labels/<int:pk>/delete/',
        LabelFormDeleteView.as_view(),
        name='delete_label'
    ),
    path(
        'tasks/create/',
        TaskFormCreateView.as_view(),
        name='create_task'
    ),
    path('tasks/', TaskIndexView.as_view(), name='task_list'),
    path(
        'tasks/<int:pk>/update/',
        TaskFormUpdateView.as_view(),
        name='update_task'
    ),
    path(
        'tasks/<int:pk>/delete',
        TaskFormDeleteView.as_view(),
        name='delete_task'
    ),
    path(
        'tasks/<int:pk>/',
        TaskView.as_view(),
        name='task_detail'
    ),


]
