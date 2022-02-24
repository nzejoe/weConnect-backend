# Generated by Django 4.0.1 on 2022-02-23 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_id',
        ),
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
        migrations.AddField(
            model_name='room',
            name='first_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='second_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_user', to=settings.AUTH_USER_MODEL),
        ),
    ]