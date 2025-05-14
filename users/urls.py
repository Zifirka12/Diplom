from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from django.urls import path

from users.views import (
    UserCreateAPIView,
    UserListAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

router = DefaultRouter()

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("user_list/", UserListAPIView.as_view(), name="user_list"),
] + router.urls
