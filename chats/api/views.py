from rest_framework import viewsets, permissions

from ..models import Chat
from .serializers import CreateChatSerializer, ChatSerializer, UpdateChatSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        match self.action:
            case 'create':
                return CreateChatSerializer
            case 'list' | 'retrieve':
                return ChatSerializer
            case 'update' | 'partial_update':
                return UpdateChatSerializer

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)
