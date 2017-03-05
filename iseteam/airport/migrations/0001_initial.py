# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PickUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=124)),
                ('last_name', models.CharField(max_length=124)),
                ('country', models.CharField(max_length=124)),
                ('email', models.EmailField(max_length=124)),
                ('flight_number', models.CharField(max_length=124)),
                ('airline', models.CharField(max_length=124)),
                ('terminal', models.CharField(max_length=124)),
                ('people', models.CharField(max_length=5, choices=[(b'1', b'ONE'), (b'2', b'TWO'), (b'3', b'THREE'), (b'4', b'FOUR'), (b'4+', b'MORE THAN 4')])),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('comments', models.CharField(max_length=1024)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attendant', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
