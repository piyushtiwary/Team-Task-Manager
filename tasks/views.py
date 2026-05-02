from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from permissions import PermissionChecker
from projects.models import Project, ProjectMember
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer

User = get_user_model()


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def get(self, request, project_id):
        project = self.get_project(project_id)

        # Check if user is project member
        if not PermissionChecker.can_view_tasks(request.user, project):
            return Response(
                {"error": "Only project members can view tasks"},
                status=status.HTTP_403_FORBIDDEN,
            )

        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = self.get_project(project_id)

        # Check if user is project admin
        if not PermissionChecker.can_create_task(request.user, project):
            return Response(
                {"error": "Only project admins can create tasks"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskCreateSerializer(
            data=request.data, context={"project": project}
        )
        if serializer.is_valid():
            task = serializer.save(project=project, created_by=request.user)
            return Response(
                {
                    "message": "Task created successfully",
                    "task": TaskSerializer(task).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_task(self, task_id):
        return get_object_or_404(Task, id=task_id)

    def patch(self, request, task_id):
        task = self.get_task(task_id)
        project = task.project

        # Check if user is project member
        if not PermissionChecker.can_view_tasks(request.user, project):
            return Response(
                {"error": "Only project members can update tasks"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if user can update this specific task
        if not PermissionChecker.can_update_task(request.user, task):
            return Response(
                {"error": "Only assigned user or admin can update this task"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Assigned users can only update status
        if PermissionChecker.can_update_task_status_only(request.user, task):
            if "status" in request.data:
                # Only allow status update
                allowed_fields = {"status"}
                provided_fields = set(request.data.keys())
                if not provided_fields.issubset(allowed_fields):
                    return Response(
                        {"error": "Assigned users can only update the status field"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            return Response(
                {
                    "message": "Task updated successfully",
                    "task": TaskSerializer(task).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = self.get_task(task_id)

        # Check if user can delete this task
        if not PermissionChecker.can_delete_task(request.user, task):
            return Response(
                {"error": "Only project admins can delete tasks"},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.delete()
        return Response(
            {"message": "Task deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# Template-based Views for Frontend


@method_decorator(login_required(login_url="login"), name="dispatch")
class TaskCreateTemplateView(View):
    """Create a new task in a project"""

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if not PermissionChecker.can_create_task(request.user, project):
            messages.error(request, "Only admins can create tasks.")
            return redirect("project-detail", project.id)

        return render(request, "task_form.html", {"project": project, "task": None})

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if not PermissionChecker.can_create_task(request.user, project):
            messages.error(request, "Only admins can create tasks.")
            return redirect("project-detail", project.id)

        title = request.POST.get("title")
        description = request.POST.get("description", "")
        status_value = request.POST.get("status", "todo")
        assigned_to_email = request.POST.get("assigned_to_email", "")
        due_date = request.POST.get("due_date", None)

        if not title or not title.strip():
            messages.error(request, "Task title is required.")
            return render(request, "task_form.html", {"project": project, "task": None})

        assigned_to = None
        if assigned_to_email:
            try:
                assigned_to = User.objects.get(email=assigned_to_email)
                if not ProjectMember.objects.filter(
                    user=assigned_to, project=project
                ).exists():
                    messages.error(request, "Assigned user must be a project member.")
                    return render(
                        request, "task_form.html", {"project": project, "task": None}
                    )
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return render(
                    request, "task_form.html", {"project": project, "task": None}
                )

        task = Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status_value,
            assigned_to=assigned_to,
            due_date=due_date or None,
            created_by=request.user,
        )
        messages.success(request, "Task created successfully!")
        return redirect("project-detail", project.id)


@method_decorator(login_required(login_url="login"), name="dispatch")
class TaskEditTemplateView(View):
    """Edit an existing task"""

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if not PermissionChecker.can_update_task(request.user, task):
            messages.error(request, "You don't have permission to edit this task.")
            return redirect("project-detail", task.project.id)

        return render(
            request,
            "task_form.html",
            {"task": task, "project": task.project},
        )

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if not PermissionChecker.can_update_task(request.user, task):
            messages.error(request, "You don't have permission to edit this task.")
            return redirect("project-detail", task.project.id)

        # Check if user can only update status
        if PermissionChecker.can_update_task_status_only(request.user, task):
            # Only update status
            status_value = request.POST.get("status")
            if status_value:
                task.status = status_value
                task.save()
        else:
            # Admin can update everything
            title = request.POST.get("title")
            if title and title.strip():
                task.title = title
            task.description = request.POST.get("description", "")
            task.status = request.POST.get("status", task.status)
            task.due_date = request.POST.get("due_date") or None

            assigned_to_email = request.POST.get("assigned_to_email", "")
            if assigned_to_email:
                try:
                    user = User.objects.get(email=assigned_to_email)
                    if ProjectMember.objects.filter(
                        user=user, project=task.project
                    ).exists():
                        task.assigned_to = user
                except User.DoesNotExist:
                    messages.error(request, "User not found.")
                    return render(
                        request,
                        "task_form.html",
                        {"task": task, "project": task.project},
                    )
            else:
                task.assigned_to = None

            task.save()

        messages.success(request, "Task updated successfully!")
        return redirect("project-detail", task.project.id)


@method_decorator(login_required(login_url="login"), name="dispatch")
class TaskDeleteTemplateView(View):
    """Delete a task"""

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if not PermissionChecker.can_delete_task(request.user, task):
            messages.error(request, "Only admins can delete tasks.")
            return redirect("project-detail", task.project.id)

        project_id = task.project.id
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("project-detail", project_id)
