from django.contrib import admin

from .models import Statuses


@admin.register(Statuses)
class UserAdmin(admin.ModelAdmin):
    pass
