from task_manager.statuses.views import (
    StatusesListView,
    StatusesUpdateView,
    StatusesCreateView,
    StatusesDeleteView,
)
from django.urls import path


app_name = "statuses"


urlpatterns = [
    path("", StatusesListView.as_view(), name="list"),
    path("create/", StatusesCreateView.as_view(), name="create"),
    path("<int:pk>/update/", StatusesUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", StatusesDeleteView.as_view(), name="delete"),
]
