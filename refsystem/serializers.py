from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from refsystem.models import UsedCode, InviteCode


class UsedCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=6,
    )

    class Meta:
        model = UsedCode
        fields = ('code', )

    def validate(self, attrs):
        user = getattr(self.context['request'], 'user', None)
        self.code = attrs.get('code')
        if UsedCode.objects.filter(user=user).exists():
            raise serializers.ValidationError('Инвайт-код уже был указан ранее')
        if self.code == InviteCode.objects.get_or_create(user=user)[0].code:
            raise serializers.ValidationError('Указан личный инвайт-код пользователя')
        if not InviteCode.objects.filter(code=self.code) or self.code != 6:
            raise serializers.ValidationError('Код не найден')
        return attrs

    def set_code(self):
        user = getattr(self.context['request'], 'user', None)
        gotten_code = self.code
        code = InviteCode.objects.filter(code=gotten_code).first()
        used_code = UsedCode.objects.create(code=code, user=user)
        used_code.save()
        return {
            'result': 'Инвайт-код успешно применен'
        }
