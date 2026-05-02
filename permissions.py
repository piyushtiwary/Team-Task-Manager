from django.shortcuts import get_object_or_404
from projects.models import ProjectMember, Project
from tasks.models import Task


class PermissionChecker:
    """Centralized permission checks for role-based access control"""

    @staticmethod
    def is_project_member(user, project):
        """Check if user is a member of the project"""
        return ProjectMember.objects.filter(user=user, project=project).exists()

    @staticmethod
    def is_project_admin(user, project):
        """Check if user is an admin in the project"""
        return ProjectMember.objects.filter(
            user=user, project=project, role="admin"
        ).exists()

    @staticmethod
    def is_task_assigned_to_user(user, task):
        """Check if user is assigned to the task"""
        return task.assigned_to == user

    @staticmethod
    def can_view_project(user, project):
        """Check if user can view the project (must be a member)"""
        return PermissionChecker.is_project_member(user, project)

    @staticmethod
    def can_edit_project(user, project):
        """Check if user can edit project (must be admin)"""
        return PermissionChecker.is_project_admin(user, project)

    @staticmethod
    def can_manage_project_members(user, project):
        """Check if user can add/remove members (must be admin)"""
        return PermissionChecker.is_project_admin(user, project)

    @staticmethod
    def can_view_tasks(user, project):
        """Check if user can view tasks (must be project member)"""
        return PermissionChecker.is_project_member(user, project)

    @staticmethod
    def can_create_task(user, project):
        """Check if user can create tasks (must be project admin)"""
        return PermissionChecker.is_project_admin(user, project)

    @staticmethod
    def can_update_task(user, task):
        """Check if user can update task (admin or assigned user)"""
        project = task.project
        is_admin = PermissionChecker.is_project_admin(user, project)
        is_assigned = PermissionChecker.is_task_assigned_to_user(user, task)
        return is_admin or is_assigned

    @staticmethod
    def can_delete_task(user, task):
        """Check if user can delete task (must be project admin)"""
        return PermissionChecker.is_project_admin(user, task.project)

    @staticmethod
    def can_update_task_status_only(user, task):
        """Check if user can only update task status (assigned user, not admin)"""
        is_admin = PermissionChecker.is_project_admin(user, task.project)
        is_assigned = PermissionChecker.is_task_assigned_to_user(user, task)
        return is_assigned and not is_admin

    @staticmethod
    def get_user_role_in_project(user, project):
        """Get user's role in the project (admin, member, or None)"""
        try:
            member = ProjectMember.objects.get(user=user, project=project)
            return member.role
        except ProjectMember.DoesNotExist:
            return None
