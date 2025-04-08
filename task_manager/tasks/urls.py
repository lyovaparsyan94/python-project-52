from django.urls import path
from task_manager.tasks.views import (
    TasksCreate,
    TasksDelete,
    TasksListView,
    TasksUpdate,
    TaskClick,
)

app_name = "tasks"

urlpatterns = [
    path("", TasksListView.as_view(), name="list"),
    path("create/", TasksCreate.as_view(), name="create"),
    path("<int:pk>/update/", TasksUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", TasksDelete.as_view(), name="delete"),
    path("<int:pk>/", TaskClick.as_view(), name="click"),
]
