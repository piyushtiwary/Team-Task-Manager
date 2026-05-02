from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.CharField(
        source="assigned_to.email", read_only=True
    )
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "assigned_to_email",
            "due_date",
            "created_by_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_by", "created_at", "updated_at")


class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(required=False, write_only=True)

    class Meta:
        model = Task
        fields = ("title", "description", "status", "assigned_to_email", "due_date")

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Task title cannot be empty.")
        return value

    def validate_status(self, value):
        valid_statuses = ["todo", "in_progress", "done"]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value

    def create(self, validated_data):
        assigned_to_email = validated_data.pop("assigned_to_email", None)
        task = Task(**validated_data)
        project = self.context.get("project")

        if assigned_to_email:
            from django.contrib.auth import get_user_model
            from projects.models import ProjectMember

            User = get_user_model()
            try:
                user = User.objects.get(email=assigned_to_email)

                # Validate assigned user is project member
                if (
                    project
                    and not ProjectMember.objects.filter(
                        user=user, project=project
                    ).exists()
                ):
                    raise serializers.ValidationError(
                        {
                            "assigned_to_email": "User must be a member of the project to be assigned a task."
                        }
                    )

                task.assigned_to = user
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"assigned_to_email": "User with this email does not exist"}
                )

        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(required=False, write_only=True)

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "assigned_to_email",
            "due_date",
        )

    def validate_title(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Task title cannot be empty.")
        return value

    def validate_status(self, value):
        if value:
            valid_statuses = ["todo", "in_progress", "done"]
            if value not in valid_statuses:
                raise serializers.ValidationError(
                    f"Status must be one of: {', '.join(valid_statuses)}"
                )
        return value

    def update(self, instance, validated_data):
        assigned_to_email = validated_data.pop("assigned_to_email", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if assigned_to_email:
            from django.contrib.auth import get_user_model
            from projects.models import ProjectMember

            User = get_user_model()
            try:
                user = User.objects.get(email=assigned_to_email)

                # Validate assigned user is project member
                project = instance.project
                if not ProjectMember.objects.filter(
                    user=user, project=project
                ).exists():
                    raise serializers.ValidationError(
                        {
                            "assigned_to_email": "User must be a member of the project to be assigned a task."
                        }
                    )

                instance.assigned_to = user
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"assigned_to_email": "User with this email does not exist"}
                )

        return instance
