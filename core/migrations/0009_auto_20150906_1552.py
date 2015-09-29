# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_bidrag_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidrag',
            name='creator',
        ),
        migrations.AddField(
            model_name='bidrag',
            name='user',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=False,
        ),
    ]
