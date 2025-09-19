from django.contrib import admin

from .models import Labels


@admin.register(Labels)
class UserAdmin(admin.ModelAdmin):
    pass
