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


# class UserDetailViewSet(mixins.RetrieveModelMixin,
#                         GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer
#
#     def get_object(self):
#         phone_number = self.kwargs.get('phone_number')
#         if phone_number == 'me':
#             return self.request.user
#         phone_number = UserServices.standardize_phone_number(phone_number)
#         user = User.objects.filter(phone_number=phone_number).first()
#         if user:
#             return user
#         raise ValidationError('Пользователя с указанным номером не существует')


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone_number'

    def get_serializer_class(self):
        if self.action == 'retrieve':  # noqa
            return UserDetailSerializer
        return UserSerializer

    def get_object(self):
        phone_number = self.kwargs.get('phone_number')
        user = self.request.user
        if phone_number == 'me' and user.is_authenticated:
            return user
        return super().get_object()

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
