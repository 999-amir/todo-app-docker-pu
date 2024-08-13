from django.urls import path
from .. import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "user"

urlpatterns = [
    path(
        "registration/",
        views.RegistrationAPIView.as_view(),
        name="registration",
    ),
    path(
        "activation/confirm/<str:token>",
        views.ActivationAPIView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        views.ActivationResendAPIView.as_view(),
        name="activation-resend",
    ),
    path(
        "forget-password/",
        views.ForgetPasswordAPIView.as_view(),
        name="forget-password",
    ),
    path(
        "forget-password/confirm/<str:token>",
        views.ConfirmForgetPasswordAPIView.as_view(),
        name="confirm-forget-password",
    ),
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
