from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConversationViewSet,
    MessageViewSet,
    ClientPropertyInterestViewSet,
    client_dashboard
)

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'interests', ClientPropertyInterestViewSet, basename='client-interest')

urlpatterns = [
    path('', include(router.urls)),
    path('client-dashboard/', client_dashboard, name='client-dashboard'),
]

