from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "assigned_to",
        "due_date",
        "created_at",
    )
    list_filter = ("status", "created_at", "due_date", "project")
    search_fields = ("title", "description", "project__name")
    ordering = ("-created_at",)

    fieldsets = (
        ("Task Info", {"fields": ("title", "description", "project")}),
        ("Assignment", {"fields": ("assigned_to", "created_by")}),
        ("Status", {"fields": ("status", "due_date")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")
