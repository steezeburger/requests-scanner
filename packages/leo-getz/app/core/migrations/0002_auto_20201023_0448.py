# Generated by Django 3.1.2 on 2020-10-23 04:48

import core.managers.user_manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.managers.user_manager.UserManager()),
            ],
        ),
    ]
