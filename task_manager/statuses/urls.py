from django.urls import path

from task_manager.statuses.views import (
    IndexView,
    StatusCreateView,
    StatusDeleteView,
    StatusUpdateView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='all_statuses'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:id>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:id>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]