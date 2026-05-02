from rest_framework import serializers
from .models import Project, ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = ProjectMember
        fields = ("id", "user_email", "user_name", "role", "joined_at")
        read_only_fields = ("joined_at",)


class ProjectSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "created_by_email",
            "members",
            "created_at",
        )
        read_only_fields = ("created_by", "created_at")

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Project name cannot be empty.")
        return value


class AddMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=["admin", "member"], default="member")

    def validate_role(self, value):
        if value not in ["admin", "member"]:
            raise serializers.ValidationError("Role must be 'admin' or 'member'")
        return value
