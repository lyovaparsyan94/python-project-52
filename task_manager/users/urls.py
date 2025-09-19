from django.urls import path


def get_url_patterns():
    from task_manager.users.views import (UserCreateView, UserDeleteView, UsersView,
                        UserUpdateView)

    return [
        path('', UsersView.as_view(), name='usrs'),
        path('create/', UserCreateView.as_view(), name='create_user'),
        path(
            'create/<int:pk>/update/',
            UserUpdateView.as_view(),
            name='update_user'),
        path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    ]


urlpatterns = get_url_patterns()