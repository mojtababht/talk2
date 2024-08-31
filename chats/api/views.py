from rest_framework import viewsets, permissions

from ..models import Chat, Message
from .serializers import CreateChatSerializer, ChatSerializer, UpdateChatSerializer, CreateMessageSerializer, \
    MessageSerializer
from reusable.paginations import DefaultPagination


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.prefetch_related('members', 'members__profile').all()
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = DefaultPagination

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


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Message.objects.filter(chat=self.kwargs['chat_pk']).select_related('chat')

    def get_serializer_class(self):
        match self.action:
            case 'create':
                return CreateMessageSerializer
            case 'list' | 'retrieve':
                return MessageSerializer
            case 'update' | 'partial_update':
                return CreateMessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'chat_id': self.kwargs['chat_pk']})
        return context

