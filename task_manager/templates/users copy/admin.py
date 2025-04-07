from django.contrib import admin
from task_manager.users.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
