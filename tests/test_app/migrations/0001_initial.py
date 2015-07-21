from __future__ import unicode_literals

import datetime

from django.conf import settings
import django.core.validators
from django.db import models, migrations
import django.utils.timezone
import guardian.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
            bases=(models.Model,),
        ),
    ]
