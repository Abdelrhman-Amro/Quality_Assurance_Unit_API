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

    n_of_course_files = serializers.SerializerMethodField()
    n_of_course_files_uploaded = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "code",
            "level",
            "semester",
            "credit_hours",
            "department",
            "academic_year",
            "professor",
            "professor_id",
            "n_of_course_files",
            "n_of_course_files_uploaded",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        level = data.get("level")
        department = data.get("department")
        if department is not None and (level is None or level <= 2):
            raise serializers.ValidationError({"department": "Department can only be set if level is greater than 2."})
        return data

    def get_n_of_course_files(self, obj):
        """Get the number of course files associated with the course."""
        return obj.files.count()

    def get_n_of_course_files_uploaded(self, obj):
        """Get the number of course files uploaded in the course."""
        attachments = CourseAttachment.objects.filter(course_file__course=obj)
        count = 0
        for attachment in attachments:
            if attachment.file:
                count += 1
        return count


class CourseFileSerializer(serializers.ModelSerializer):
    """Serializer for CourseFile model."""

    attachments = serializers.SerializerMethodField()

    class Meta:
        model = CourseFile
        fields = ["id", "title", "course", "created_at", "updated_at", "attachments"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_attachments(self, obj):
        attachments = CourseAttachment.objects.filter(course_file=obj)
        return CourseAttachmentSerializer(attachments, many=True, context=self.context).data


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
