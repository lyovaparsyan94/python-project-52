from django.contrib import admin
from django.urls import path
from task_manager.labels.views import LabelsListView, LabelsCreate, LabelsUpdate, LabelsDelete


app_name = 'labels'


urlpatterns = [
    path('', LabelsListView.as_view(), name='list'),
    path('create/', LabelsCreate.as_view(), name='create'),
    path('<int:pk>/update/', LabelsUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', LabelsDelete.as_view(), name='delete'),

]