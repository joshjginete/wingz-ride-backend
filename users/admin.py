from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ["id", "username", "phone_number"]
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "user_role",
    ]


admin.site.register(User, UserAdmin)
