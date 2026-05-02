from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
)

urlpatterns = [
    # API endpoints (under /api/tasks/)
    path(
        "projects/<int:project_id>/tasks/",
        TaskListCreateView.as_view(),
        name="api-task-list-create",
    ),
    path("tasks/<int:task_id>/", TaskDetailView.as_view(), name="api-task-detail"),
]
