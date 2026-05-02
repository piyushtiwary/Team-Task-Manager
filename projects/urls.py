from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    AddProjectMemberView,
    RemoveProjectMemberView,
)

urlpatterns = [
    # API endpoints (under /api/projects/)
    path("", ProjectListCreateView.as_view(), name="api-project-list-create"),
    path("<int:project_id>/", ProjectDetailView.as_view(), name="api-project-detail"),
    path(
        "<int:project_id>/add-member/",
        AddProjectMemberView.as_view(),
        name="api-add-member",
    ),
    path(
        "<int:project_id>/members/<int:member_id>/",
        RemoveProjectMemberView.as_view(),
        name="api-remove-member",
    ),
]
