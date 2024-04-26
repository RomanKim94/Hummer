from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    phone_number = models.CharField(
        verbose_name='Номер телефона пользователя',
        max_length=15,
        unique=True,
    )
    USERNAME_FIELD = 'phone_number'


class RegCode(models.Model):
    reg_code = models.CharField(
        verbose_name='Код авторизации',
        max_length=4,
    )
    user = models.OneToOneField(
        'User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='reg_code'
    )
    creation_time = models.DateTimeField(
        verbose_name='Время создания кода',
        auto_now=True,
        blank=True,
        null=True,
    )
