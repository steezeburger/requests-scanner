# Generated by Django 3.1.2 on 2020-10-30 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_requests', '0002_auto_20201030_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plexmovie',
            name='year',
            field=models.SmallIntegerField(blank=True, db_index=True, help_text='The year the movie was released.', null=True),
        ),
    ]
