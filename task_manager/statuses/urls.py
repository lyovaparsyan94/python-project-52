from django.urls import path

from .views import (
    CreateStatusesView,
    DeleteStatusesView,
    IndexStatusesView,
    UpdateStatusesView,
)

urlpatterns = [
    path('', IndexStatusesView.as_view(), name='statuses'),
    path('create/', CreateStatusesView.as_view(), name='create_status'),
    path(
        '<int:pk>/update/', UpdateStatusesView.as_view(), name='update_status'
    ),
    path(
        '<int:pk>/delete/', DeleteStatusesView.as_view(), name='delete_status'
    ),
]