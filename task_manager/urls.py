from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from task_manager.labels import views as labels_views
from task_manager.statuses import views as statuses_views
from task_manager.tasks import views as tasks_views
from task_manager.users import views as users_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', tasks_views.index, name='home'),
    path('users/', users_views.UserListView.as_view(), name='users_list'),
    path('users/create/', users_views.UserCreateView.as_view(),
          name='user_create'),
    path('users/<int:pk>/update/', users_views.UserUpdateView.as_view(),
          name='user_update'),
    path('users/<int:pk>/delete/', users_views.UserDeleteView.as_view(),
          name='user_delete'),
    path('login/', users_views.CustomLoginView.as_view(), name='login'),
    path('logout/', users_views.custom_logout, name='logout'),
    path('statuses/', statuses_views.StatusListView.as_view(),
          name='statuses_list'),
    path('statuses/create/', statuses_views.StatusCreateView.as_view(),
          name='status_create'),
    path('statuses/<int:pk>/update/', statuses_views.StatusUpdateView.as_view(),
          name='status_update'),
    path('statuses/<int:pk>/delete/', statuses_views.StatusDeleteView.as_view(),
          name='status_delete'),
    path('tasks/', tasks_views.TaskListView.as_view(), name='tasks_list'),
    path('tasks/create/', tasks_views.TaskCreateView.as_view(),
          name='task_create'),
    path('tasks/<int:pk>/', tasks_views.TaskDetailView.as_view(),
          name='task_detail'),
    path('tasks/<int:pk>/update/', tasks_views.TaskUpdateView.as_view(),
          name='task_update'),
    path('tasks/<int:pk>/delete/', tasks_views.TaskDeleteView.as_view(),
          name='task_delete'),
    path('labels/', labels_views.LabelListView.as_view(), name='labels_list'),
    path('labels/create/', labels_views.LabelCreateView.as_view(),
          name='label_create'),
    path('labels/<int:pk>/update/', labels_views.LabelUpdateView.as_view(),
          name='label_update'),
    path('labels/<int:pk>/delete/', labels_views.LabelDeleteView.as_view(),
          name='label_delete'),
    path('debug/', tasks_views.debug_lang, name='debug_lang'),
)
