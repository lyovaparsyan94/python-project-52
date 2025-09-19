from django.urls import path

from .views import LabelCreate, LabelDelete, LabelsView, LabelUpdate

urlpatterns = [
    path('', LabelsView.as_view(), name='labels'),
    path('<int:pk>/update/', LabelUpdate.as_view(), name='update_label'),
    path('create/', LabelCreate.as_view(), name='create_label'),
    path('<int:pk>/delete/', LabelDelete.as_view(), name='delete_label'),
]
