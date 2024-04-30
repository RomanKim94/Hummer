from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from refsystem.models import InviteCode, UsedCode
from user.Services import UserServices
from user.models import User, RegCode


class UserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=17)
    reg_code = serializers.CharField(max_length=4, required=False)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        phone_number = UserServices.standardize_phone_number(phone_number)
        self.phone_number = phone_number
        return attrs

    def send_reg_code(self):
        self.user, created = User.objects.get_or_create(phone_number=self.phone_number)
        if created:
            self.user.save()
        reg_code_obj = RegCode.objects.get_or_create(user=self.user, defaults={'reg_code': ''})[0]
        reg_code_obj.reg_code = UserServices.get_digit_code(digit_quantity=4)
        reg_code_obj.save()
        UserServices.send_sms(self.user.phone_number)
        return {
            'sms': reg_code_obj.reg_code
        }


class ProvingRegCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    reg_code = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        reg_code = attrs.get('reg_code')

        phone_number = UserServices.standardize_phone_number(phone_number)

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError({'phone_number': 'Пользователь с таким номером телефона не найден.'})
        reg_code_object = RegCode.objects.filter(user=user).first()
        if not reg_code_object:
            raise serializers.ValidationError({'reg_code': 'Код не подходит.'})
        if reg_code_object.reg_code != reg_code:
            raise serializers.ValidationError({'reg_code': 'Код не подходит.'})
        if not timedelta(minutes=5) > timezone.now() - reg_code_object.creation_time:
            raise serializers.ValidationError({'reg_code': 'Срок действия кода истек.'})
        self.user = user
        self.reg_code = reg_code_object

        return attrs

    def get_auth_tokens(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create_invite_code(self):
        code = InviteCode.objects.create(user=self.user, code=UserServices.generate_invite_code(symbol_quantity=6))
        code.save()


class UserDetailSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    invite_code = serializers.SerializerMethodField()
    strange_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'invited_users', 'strange_code')

    def get_invite_code(self, obj):
        invite_code_obj = InviteCode.objects.get(user=obj)
        return invite_code_obj.code

    def get_invited_users(self, obj):
        invite_code = InviteCode.objects.filter(user=obj).first()
        users = [user.phone_number for user in User.objects.filter(used_code__code=invite_code)]
        return users

    def get_strange_code(self, obj):
        strange_code = UsedCode.objects.filter(user=obj).first()
        if strange_code:
            return strange_code.code.code
        return None