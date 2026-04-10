from django.contrib import admin
from .models import Status
from tasks.models import Task

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
