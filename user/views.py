from datetime import datetime, timedelta

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from user.Services import UserServices
from user.models import User, RegCode
from user.serializers import UserSerializer, ProvingRegCodeSerializer, UserDetailSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':  # noqa
            return UserDetailSerializer
        return UserSerializer


    @action(methods=['POST'], detail=False)
    def send_reg_code(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.send_reg_code()
        return Response(response_data)

    @action(methods=['POST'], detail=False)
    def send_access_token(self, request):
        serializer = ProvingRegCodeSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.get_auth_tokens()
        return Response(response_data)
