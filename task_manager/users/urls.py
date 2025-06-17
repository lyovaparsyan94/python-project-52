from django.urls import path
from task_manager.users import views

app_name = 'users'

urlpatterns = [
    path('create/',
         views.CreateUserView.as_view(), name='create_user'),
    path('<int:id>/update/',
         views.UpdateUserView.as_view(), name='update_user'),
    path('<int:id>/delete/',
         views.DeleteUserView.as_view(), name='delete_user'),
    path('',
         views.IndexView.as_view(), name='users'),
]
