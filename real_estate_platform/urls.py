"""
URL configuration for real_estate_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate Platform API",
        default_version='v1',
        description="API documentation for Real Estate Software Platform",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@realestate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API Endpoints
    path('api/auth/', include('users.urls')),
    path('api/materials/', include('materials.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/estimates/', include('cost_estimates.urls')),
    path('api/pages/', include('pages.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/activity-logs/', include('activity_log.urls')),
    path('api/search/', include('search.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/messaging/', include('messaging.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
