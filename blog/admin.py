from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "created_at",
    )