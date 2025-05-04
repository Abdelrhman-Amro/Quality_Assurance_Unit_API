from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()

# Viewset for admin users only to work on full CRUD operations and users data
#


class UserViewSet(ModelViewSet):
    """
    ViewSet for the User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role"]
    ordering_fields = ["username", "last_login", "date_joined"]
    search_fields = ["username"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "role",
                openapi.IN_QUERY,
                description="Filter by role",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in User.Role.choices],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserRetrieveView(RetrieveAPIView):
    """
    View for retrieving user details.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
