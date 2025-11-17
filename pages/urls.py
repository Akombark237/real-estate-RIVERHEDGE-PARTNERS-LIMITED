from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutPageViewSet, TeamMemberViewSet

router = DefaultRouter()
router.register(r'about', AboutPageViewSet, basename='about')
router.register(r'team', TeamMemberViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]

