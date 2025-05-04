from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# 🎯 Define API schema
schema_view = get_schema_view(
    openapi.Info(
        title="Quality Assurance Unit - API",
        default_version="v1",
        description="API documentation for the Quality Assurance Unit system in colleges.",
        # terms_of_service="https://www.example.com/terms/",
        # contact=openapi.Contact(email="contact@example.com"),
        # license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Anyone can see docs
)

# 🌍 Add URLs for Swagger & ReDoc
urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),  # Swagger UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),  # ReDoc UI
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # Raw JSON/YAML
]

# # 🌐 Add URLs for Spectacular (if using it instead of drf_yasg)
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularRedocView,
#     SpectacularSwaggerView,
# )

# urlpatterns += [
#     # YOUR PATTERNS
#     path("schema/", SpectacularAPIView.as_view(), name="schema"),
#     # Optional UI:
#     path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
#     path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
# ]
