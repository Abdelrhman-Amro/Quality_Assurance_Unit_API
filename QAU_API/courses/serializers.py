from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course, CourseAttachment, CourseFile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (minimal version for nested relationships)."""

    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""

    professor = UserSerializer(read_only=True)
    professor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        source="professor",
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "code",
            "level",
            "semester",
            "credit_hours",
            "academic_year",
            "professor",
            "professor_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CourseFileSerializer(serializers.ModelSerializer):
    """Serializer for CourseFile model."""

    class Meta:
        model = CourseFile
        fields = ["id", "title", "course", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CourseAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for CourseAttachment model."""

    class Meta:
        model = CourseAttachment
        fields = [
            "id",
            "course_file",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_file(self, value):
        """Validate that file is provided."""
        if not value:
            raise serializers.ValidationError("File is required.")
        return value
