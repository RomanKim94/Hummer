# Generated by Django 4.2 on 2024-04-24 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regcode',
            name='creation_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Время создания кода'),
        ),
    ]