from django.urls import path

from task_manager.tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TasksView,
    TaskShowView,
    TaskUpdateView,
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('<int:pk>/', TaskShowView.as_view(), name='view_task'),
]