from django.urls import path

from .views import (
    CreateLabelsView,
    DeleteLabelsView,
    IndexLabelsView,
    UpdateLabelsView,
)

urlpatterns = [
    path('', IndexLabelsView.as_view(), name='labels'),
    path('create/', CreateLabelsView.as_view(), name='create_label'),
    path(
        '<int:pk>/update/', UpdateLabelsView.as_view(), name='update_label'
    ),
    path(
        '<int:pk>/delete/', DeleteLabelsView.as_view(), name='delete_label'
    ),
]