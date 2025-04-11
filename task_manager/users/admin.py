# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# # Unregister the provided model admin
# admin.site.unregister(get_user_model())


# # Register out own model admin, based on the default UserAdmin
# @admin.register(get_user_model())
# class CustomUserAdmin(UserAdmin):
#     list_display = [
#         "username",
#         "email",
#         "last_name",
#         "first_name",
#         "last_login",
#         "date_joined",
#     ]
#     search_fields = [
#         "username",
#         "email",
#         "last_name",
#         "first_name",
#     ]
