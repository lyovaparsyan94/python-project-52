from django.urls import path
from task_manager.users.views import (
    UsersListView,
    UsersCreate,
    UsersUpdate,
    UsersDelete,
)


app_name = "users"


urlpatterns = [
    path("", UsersListView.as_view(), name="list"),
    path("create/", UsersCreate.as_view(), name="create"),
    path("<int:pk>/update/", UsersUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", UsersDelete.as_view(), name="delete"),
]
