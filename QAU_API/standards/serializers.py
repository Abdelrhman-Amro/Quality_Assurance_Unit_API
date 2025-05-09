from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AcademicYear, Attachment, Element, Pointer, Request, Standard

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (minimal version for nested relationships)."""

    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class AcademicYearSerializer(serializers.ModelSerializer):
    """Serializer for AcademicYear model."""

    class Meta:
        model = AcademicYear
        fields = ["id", "status", "start_date", "end_date", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        """Validate that start_date is before end_date."""
        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] >= data["end_date"]:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )
        return data


class StandardSerializer(serializers.ModelSerializer):
    """Serializer for Standard model."""

    assigned_to = UserSerializer(many=True, read_only=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        many=True,
        required=False,
        source="assigned_to",
    )

    class Meta:
        model = Standard
        fields = [
            "id",
            "title",
            "type",
            "academic_year",
            "assigned_to",
            "assigned_to_ids",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PointerSerializer(serializers.ModelSerializer):
    """Serializer for Pointer model."""

    class Meta:
        model = Pointer
        fields = ["id", "title", "standard", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ElementSerializer(serializers.ModelSerializer):
    """Serializer for Element model."""

    class Meta:
        model = Element
        fields = ["id", "title", "pointer", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class AttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Attachment model."""

    uploaded_by = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)
    shared_with_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        many=True,
        required=False,
        source="shared_with",
    )

    class Meta:
        model = Attachment
        fields = [
            "id",
            "title",
            "file",
            "element",
            "uploaded_by",
            "shared_with",
            "shared_with_ids",
            "uploaded_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_at",
            "created_at",
            "updated_at",
        ]

    def validate_file(self, value):
        """Validate that file is provided."""
        if not value:
            raise serializers.ValidationError("File is required.")
        return value


class RequestSerializer(serializers.ModelSerializer):
    """Serializer for Request model."""

    requester = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Request
        fields = [
            "id",
            "requester",
            "receiver",
            "made_on",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "requester",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_made_on(self, value):
        """Validate that the attachment has a file and was uploaded by someone."""
        if not value.file:
            raise serializers.ValidationError("Attachment must have a file.")
        if not value.uploaded_by:
            raise serializers.ValidationError("Attachment must have an uploader.")
        return value


class RequestDetailSerializer(RequestSerializer):
    """Detailed serializer for Request model with attachment details."""

    made_on = AttachmentSerializer(read_only=True)

    class Meta(RequestSerializer.Meta):
        fields = RequestSerializer.Meta.fields
        read_only_fields = RequestSerializer.Meta.read_only_fields + ["made_on"]
