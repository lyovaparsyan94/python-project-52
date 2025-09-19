from django.contrib import admin

from .models import Tasks


@admin.register(Tasks)
class UserAdmin(admin.ModelAdmin):
    pass
