from rest_framework.routers import DefaultRouter

from .views import ChatViewSet

router = DefaultRouter()
router.register('chats', ChatViewSet)
