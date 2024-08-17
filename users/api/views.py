from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import LoginSerializer, SignUpSerializer, UserSerializer
from .permissions import NeedToNotAuthenticate
from ..models import User


class AuthViewSet(viewsets.ViewSet):
    # permission_classes = (NeedToNotAuthenticate,)

    @swagger_auto_schema(method='post', request_body=LoginSerializer, responses={
        status.HTTP_200_OK: "{'access': 'string', 'refresh': 'string'}",
        status.HTTP_403_FORBIDDEN: "Incorrect authentication credentials."
    })
    @action(methods=('post',), detail=False, url_name='login')
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = User.login(**serializer.validated_data)
        return Response(response, status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=SignUpSerializer)  # TODO: fix response schema
    @action(methods=('post',), detail=False, url_name='signup')
    def signup(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.pop('password_repeat')
        response, status_code = User.signup(data)
        return Response(response, status_code)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(id=self.request.user.id)

    @action(methods=('get',), detail=False, url_name='user-info')
    def user_info(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request, 'view': self})
        return Response(serializer.data)

