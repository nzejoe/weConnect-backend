# Generated by Django 4.0.1 on 2022-02-02 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_userfollower'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFollower',
        ),
    ]
