from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.http import HttpResponse

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Learning Platform API",
        default_version='v1',
        description="API documentation for Learning Platform",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@learning-platform.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Приветственная страница
    path('', lambda request: HttpResponse('''
        <html>
        <head>
            <meta charset="utf-8">
            <title>Добро пожаловать!</title>
            <style>
                body { font-family: "Segoe UI", Arial, sans-serif; background: #fdf6f0; color: #222; text-align: center; margin: 0; padding: 0; }
                .welcome { margin: 60px auto 0 auto; background: #fff7f2; border-radius: 18px; box-shadow: 0 4px 24px #ffb88c33; max-width: 480px; padding: 36px 24px; }
                h1 { color: #ff7e5f; }
                a { display: block; margin: 18px auto; color: #ff7e5f; font-size: 1.2rem; text-decoration: none; border-radius: 8px; padding: 10px 0; background: #fff0e6; transition: background 0.2s; }
                a:hover { background: #ffecd2; }
            </style>
        </head>
        <body>
            <div class="welcome">
                <h1>Добро пожаловать на платформу самообучения!</h1>
                <p>Выберите раздел:</p>
                <a href="/swagger/">Документация Swagger</a>
                <a href="/redoc/">Документация ReDoc</a>
                <a href="/api/v1/">API (v1)</a>
                <a href="/admin/">Админ-панель</a>
            </div>
        </body>
        </html>
    ''', content_type="text/html; charset=utf-8")),
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API URLs
    path('api/v1/', include([
        path('users/', include('users.urls')),
        path('', include('learning_platform.urls')),
        path('', include('tests.urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
