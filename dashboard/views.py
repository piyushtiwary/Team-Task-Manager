from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tasks.models import Task
from projects.models import Project, ProjectMember


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get dashboard summary for current user"""
        user = request.user
        today = timezone.now().date()

        # Get all tasks for projects where user is a member
        user_projects = ProjectMember.objects.filter(user=user).values_list(
            "project_id", flat=True
        )
        user_tasks = Task.objects.filter(project_id__in=user_projects)

        # Calculate metrics
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(status="done").count()
        pending_tasks = user_tasks.exclude(status="done").count()

        # Overdue tasks: due_date < today AND status != 'done'
        overdue_tasks = user_tasks.filter(
            due_date__date__lt=today, status__in=["todo", "in_progress"]
        ).count()

        return Response(
            {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "overdue_tasks": overdue_tasks,
                "summary": {
                    "completion_rate": (
                        round((completed_tasks / total_tasks * 100), 2)
                        if total_tasks > 0
                        else 0
                    ),
                    "overdue_percentage": (
                        round((overdue_tasks / pending_tasks * 100), 2)
                        if pending_tasks > 0
                        else 0
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(login_required(login_url="login"), name="dispatch")
class DashboardTemplateView(View):
    """Template-based dashboard view"""

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Get projects where user is a member
        user_projects = ProjectMember.objects.filter(user=user).values_list(
            "project_id", flat=True
        )
        projects = Project.objects.filter(id__in=user_projects).prefetch_related(
            "members"
        )

        # Calculate progress for each project
        for project in projects:
            project_tasks = Task.objects.filter(project=project)
            total = project_tasks.count()
            if total > 0:
                completed = project_tasks.filter(status="done").count()
                project.progress = round((completed / total) * 100)
            else:
                project.progress = 0

        # Get all tasks for metrics
        user_tasks = Task.objects.filter(project_id__in=user_projects)
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(status="done").count()
        pending_tasks = user_tasks.exclude(status="done").count()
        overdue_tasks = user_tasks.filter(
            due_date__date__lt=today, status__in=["todo", "in_progress"]
        ).count()

        context = {
            "projects": projects[:6],  # Show first 6 projects
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "overdue_tasks": overdue_tasks,
        }

        return render(request, "dashboard.html", context)
