from django.urls import path

from task_manager.users.views import (
    DeleteUser,
    IndexUserView,
    UserRegister,
    UserUpdate,
)

urlpatterns = [
    path('', IndexUserView.as_view(), name='all_users'),
    path('create/', UserRegister.as_view(), name='user_create'),
    path('<int:id>/update/', UserUpdate.as_view(), name='user_update'),
    path('<int:id>/delete/', DeleteUser.as_view(), name='user_delete'),
]
