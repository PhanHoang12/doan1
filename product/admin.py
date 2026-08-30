from django.contrib import admin
from .models import Category, Brand, Product, History


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Brand)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
        "brand",
        "sale",
        "user",
    )
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "user",
        "price",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "user__username",
    )
    list_filter = (
        "created_at",
    )
    # Cho đơn hàng mới nhất nằm trên cùng 
    ordering =(
        "-created_at",
    )