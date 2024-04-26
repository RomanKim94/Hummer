from django.db import models


class InviteCode(models.Model):
    code = models.CharField(
        verbose_name='Личный инвайт-код пользователя',
        max_length=6,
        blank=True,
    )
    user = models.OneToOneField(
        'user.User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='invite_code',
    )


class UsedCode(models.Model):
    code = models.ForeignKey(
        'InviteCode',
        verbose_name='Чужой инвайт-код',
        on_delete=models.SET_NULL,
        related_name='usings',
        default=None,
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        'user.User',
        verbose_name='Пользователь, который использует инвайт-код',
        on_delete=models.CASCADE,
        related_name='used_code',
    )
