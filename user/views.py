from datetime import datetime, timedelta

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from user.Services import UserServices
from user.models import User, RegCode
from user.serializers import UserSerializer, ProvingRegCodeSerializer, UserDetailSerializer


class UserDetailViewSet(mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request, pk=None):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def get_object(self):
        phone_number = self.kwargs.get('phone_number')
        phone_number = UserServices.standardize_phone_number(phone_number)
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            return user
        else:
            raise ValidationError('Пользователя с указанным номером не существует')


class UserViewSet(mixins.ListModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        serializer.create_invite_code()
        response_data = serializer.get_auth_tokens()
        return Response(response_data)
