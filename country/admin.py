from django.contrib import admin

from .models import Country, CustomUser


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "level",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    ordering = (
        "-id",
    )

    def level(self, obj):

        if obj.is_staff:
            return "Admin"

        return "Member"

    level.short_description = "Level"