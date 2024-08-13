from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from todo.api.v1.permissions import IsOwner


schema_view = get_schema_view(
    openapi.Info(
        title="todo-app",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="MIT license"),
    ),
    public=True,
    permission_classes=[IsAuthenticated, IsOwner],
)

# website base urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo.urls", namespace="todo")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    # login api
    path("api-auth/", include("rest_framework.urls")),
    # api documentaion
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema_swagger_ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema_redoc_ui",
    ),
    path(
        "swagger/output.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema_json",
    ),
    # djoser authentication api
    path("djoser-accounts/", include("djoser.urls"), name="api_v2"),
    path("djoser-accounts/", include("djoser.urls.jwt"), name="api_v2"),
]

# media & static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
