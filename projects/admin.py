from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    list_filter = ("created_at", "created_by")
    search_fields = ("name", "description")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Metadata", {"fields": ("created_by", "created_at")}),
    )

    readonly_fields = ("created_at",)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "role", "joined_at")
    list_filter = ("role", "joined_at", "project")
    search_fields = ("user__email", "project__name")
    ordering = ("-joined_at",)

    fieldsets = (
        (None, {"fields": ("user", "project", "role")}),
        ("Metadata", {"fields": ("joined_at",)}),
    )

    readonly_fields = ("joined_at",)
