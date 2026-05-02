"""
URL configuration for ProjectManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    SignupTemplateView,
    LoginTemplateView,
    LogoutView,
)
from dashboard.views import DashboardTemplateView

# Import specific template views for tasks
from tasks.views import (
    TaskCreateTemplateView,
    TaskEditTemplateView,
    TaskDeleteTemplateView,
)

# Import specific template views for projects
from projects.views import (
    ProjectsTemplateView,
    ProjectCreateTemplateView,
    ProjectDetailTemplateView,
    AddMemberTemplateView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Template routes - Authentication
    path("signup/", SignupTemplateView.as_view(), name="signup"),
    path("login/", LoginTemplateView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Template routes - Dashboard
    path("dashboard/", DashboardTemplateView.as_view(), name="dashboard"),
    # Template routes - Projects
    path("projects/", ProjectsTemplateView.as_view(), name="projects"),
    path("projects/new/", ProjectCreateTemplateView.as_view(), name="project-create"),
    path(
        "projects/<int:project_id>/",
        ProjectDetailTemplateView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<int:project_id>/add-member/",
        AddMemberTemplateView.as_view(),
        name="add-member",
    ),
    # Template routes - Tasks
    path(
        "projects/<int:project_id>/tasks/create/",
        TaskCreateTemplateView.as_view(),
        name="task-create",
    ),
    path("tasks/<int:task_id>/edit/", TaskEditTemplateView.as_view(), name="task-edit"),
    path(
        "tasks/<int:task_id>/delete/",
        TaskDeleteTemplateView.as_view(),
        name="task-delete",
    ),
    # API routes
    path("api/auth/", include("accounts.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
