from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register('chats', ChatViewSet)

message_router = NestedDefaultRouter(router, 'chats', lookup='chat')
message_router.register('messages', MessageViewSet, basename='chat-messages')
