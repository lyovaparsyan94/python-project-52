from django.urls import path

from task_manager.tasks.views import (
    IndexView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='all_tasks'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:id>/', TaskView.as_view(), name='view_task'),
    path('<int:id>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:id>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]