from django.urls import path

from task_manager.labels.views import (
    IndexView,
    LabelCreateView,
    LabelDeleteView,
    LabelUpdateView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='all_labels'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('<int:id>/update/', LabelUpdateView.as_view(), name='label_update'),
    path('<int:id>/delete/', LabelDeleteView.as_view(), name='label_delete'),
]