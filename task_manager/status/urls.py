from django.urls import path

from .views import StatusCreate, StatusDelete, StatusUpdate, StatusView

urlpatterns = [
    path('', StatusView.as_view(), name='status'),
    path(
        'create/<int:pk>/update/',
        StatusUpdate.as_view(),
        name='update_status'),
    path('create/', StatusCreate.as_view(), name='create_status'),
    path('<int:pk>/delete/', StatusDelete.as_view(), name='delete_status'),
]
