from django.urls import path

from .views import TaskCreate, TaskDelete, TasksView, TaskUpdate, TaskView

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('<int:pk>/', TaskView.as_view(), name='tsk'),
    path('create/<int:pk>/update/', TaskUpdate.as_view(), name='update_task'),
    path('create/', TaskCreate.as_view(), name='create_task'),
    path('<int:pk>/delete/', TaskDelete.as_view(), name='delete_task'),

]
