# Generated by Django 4.2 on 2024-04-23 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Номер телефона пользователя')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_code', models.CharField(max_length=4, verbose_name='Код авторизации')),
                ('creation_time', models.DateTimeField(auto_now=True, verbose_name='Время создания кода')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reg_code', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]