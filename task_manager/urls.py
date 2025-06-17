from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path('', include("task_manager.tasks.urls", namespace='tasks')),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.TaskManagerLoginView.as_view(), name='login'),
    path('logout/', views.TaskManagerLogoutView.as_view(), name='logout'),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('rollbar_test/', views.rollbar_test)
]
