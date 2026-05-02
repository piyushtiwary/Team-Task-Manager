from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from permissions import PermissionChecker
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, AddMemberSerializer, ProjectMemberSerializer

User = get_user_model()


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(created_by=request.user)
            # Automatically add creator as admin
            ProjectMember.objects.create(
                user=request.user, project=project, role="admin"
            )
            return Response(
                {
                    "message": "Project created successfully",
                    "project": ProjectSerializer(project).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def get(self, request, project_id):
        project = self.get_project(project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        project = self.get_project(project_id)
        if not PermissionChecker.can_edit_project(request.user, project):
            return Response(
                {"error": "Only project admins can delete projects"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.delete()
        return Response(
            {"message": "Project deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddProjectMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def post(self, request, project_id):
        project = self.get_project(project_id)

        # Check if requester is project admin
        if not PermissionChecker.can_manage_project_members(request.user, project):
            return Response(
                {"error": "Only project admins can add members"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AddMemberSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            role = serializer.validated_data["role"]

            # Get user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check if user is already a member
            if ProjectMember.objects.filter(user=user, project=project).exists():
                return Response(
                    {"error": "User is already a member of this project"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Add member to project
            member = ProjectMember.objects.create(user=user, project=project, role=role)
            return Response(
                {
                    "message": "Member added successfully",
                    "member": ProjectMemberSerializer(member).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveProjectMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def delete(self, request, project_id, member_id):
        project = self.get_project(project_id)

        # Check if requester is project admin
        if not PermissionChecker.can_manage_project_members(request.user, project):
            return Response(
                {"error": "Only project admins can remove members"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get member
        member = get_object_or_404(ProjectMember, id=member_id, project=project)

        # Prevent removing the last admin
        admin_count = ProjectMember.objects.filter(
            project=project, role="admin"
        ).count()
        if member.role == "admin" and admin_count == 1:
            return Response(
                {"error": "Cannot remove the last admin from the project"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member.delete()
        return Response(
            {"message": "Member removed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# Template-based Views for Frontend

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProjectsTemplateView(View):
    """List all projects where user is a member"""

    def get(self, request):
        user_projects = ProjectMember.objects.filter(user=request.user).values_list(
            "project_id", flat=True
        )
        projects = Project.objects.filter(id__in=user_projects).prefetch_related(
            "members"
        )

        context = {"projects": projects}
        return render(request, "projects.html", context)


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProjectCreateTemplateView(View):
    """Create a new project"""

    def get(self, request):
        return render(request, "project_form.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description", "")

        if not name or not name.strip():
            messages.error(request, "Project name is required.")
            return render(request, "project_form.html")

        project = Project.objects.create(
            name=name, description=description, created_by=request.user
        )
        ProjectMember.objects.create(user=request.user, project=project, role="admin")
        messages.success(request, "Project created successfully!")
        return redirect("project-detail", project.id)


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProjectDetailTemplateView(View):
    """View project details and tasks"""

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        # Check if user is a member
        if not PermissionChecker.is_project_member(request.user, project):
            messages.error(request, "You don't have access to this project.")
            return redirect("projects")

        is_admin = PermissionChecker.is_project_admin(request.user, project)
        tasks = project.tasks.all()

        context = {
            "project": project,
            "tasks": tasks,
            "is_admin": is_admin,
        }
        return render(request, "project_detail.html", context)


@method_decorator(login_required(login_url="login"), name="dispatch")
class AddMemberTemplateView(View):
    """Add member to project"""

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if not PermissionChecker.can_manage_project_members(request.user, project):
            messages.error(request, "Only admins can add members.")
            return redirect("project-detail", project.id)

        return render(request, "add_member.html", {"project": project})

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if not PermissionChecker.can_manage_project_members(request.user, project):
            messages.error(request, "Only admins can add members.")
            return redirect("project-detail", project.id)

        email = request.POST.get("email")
        role = request.POST.get("role", "member")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return render(request, "add_member.html", {"project": project})

        if ProjectMember.objects.filter(user=user, project=project).exists():
            messages.error(request, "User is already a member.")
            return render(request, "add_member.html", {"project": project})

        ProjectMember.objects.create(user=user, project=project, role=role)
        messages.success(request, f"Member added successfully!")
        return redirect("project-detail", project.id)
