from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "is_staff", "role")
        read_only_fields = ("id", "is_active")
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "role": {"required": True},
            "password": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        """
        Create and return a new user
        Hashing password before saving the user
        """
        password = validated_data.pop("password", None)  # Get and Remove password
        instance = self.Meta.model(**validated_data)  # Create user instance
        if password:
            instance.set_password(password)  # Update instacne with Hashed password
        instance.save()  # save user instance
        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing user
        Hashing password before saving user
        """
        password = validated_data.pop("password", None)  # Get and Remove password
        if password:
            instance.set_password(password)  # Update instacne with Hashed password
        return super().update(instance, validated_data)
