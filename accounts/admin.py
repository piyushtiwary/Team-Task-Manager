from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("email", "name")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
        ("Important Dates", {"fields": ("created_at",)}),
    )

    readonly_fields = ("created_at",)
