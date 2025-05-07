# from django.contrib.auth import get_user_model
# from rest_framework import serializers

# from .models import AcademicYear, Attachment, Element, Pointer, Request, Standard

# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "role"]
#         read_only_fields = ["id", "username", "email", "role"]


# class AcademicYearSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AcademicYear
#         fields = ["id", "status", "start_date", "end_date", "created_at", "updated_at"]
#         read_only_fields = ["id", "created_at", "updated_at"]


# class StandardSerializer(serializers.ModelSerializer):
#     assigned_to = UserSerializer(many=True, read_only=True)
#     assigned_to_ids = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True,
#         source="assigned_to",
#         many=True,
#         required=False,
#     )

#     class Meta:
#         model = Standard
#         fields = [
#             "id",
#             "title",
#             "academic_year",
#             "assigned_to",
#             "assigned_to_ids",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["id", "created_at", "updated_at"]


# class PointerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pointer
#         fields = ["id", "title", "standard", "created_at", "updated_at"]
#         read_only_fields = ["id", "created_at", "updated_at"]


# class ElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Element
#         fields = ["id", "title", "pointer", "created_at", "updated_at"]
#         read_only_fields = ["id", "created_at", "updated_at"]


# class AttachmentSerializer(serializers.ModelSerializer):
#     uploaded_by = UserSerializer(read_only=True)
#     shared_with = UserSerializer(many=True, read_only=True)
#     shared_with_ids = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         write_only=True,
#         source="shared_with",
#         many=True,
#         required=False,
#     )
#     file = serializers.FileField(required=False)

#     class Meta:
#         model = Attachment
#         fields = [
#             "id",
#             "title",
#             "element",
#             "file",
#             "uploaded_by",
#             "shared_with",
#             "shared_with_ids",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["id", "uploaded_by", "created_at", "updated_at"]

#     def create(self, validated_data):
#         shared_with = validated_data.pop("shared_with", [])
#         attachment = Attachment.objects.create(**validated_data)
#         attachment.shared_with.set(shared_with)
#         return attachment


# class RequestSerializer(serializers.ModelSerializer):
#     requester = UserSerializer(read_only=True)
#     receiver = UserSerializer(read_only=True)
#     receiver_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), write_only=True, source="receiver"
#     )

#     class Meta:
#         model = Request
#         fields = [
#             "id",
#             "requester",
#             "receiver",
#             "receiver_id",
#             "made_on",
#             "status",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["id", "requester", "status", "created_at", "updated_at"]
