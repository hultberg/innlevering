# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151001_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidrag',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='bidrag',
            unique_together=set([('compo', 'creator')]),
        ),
    ]
