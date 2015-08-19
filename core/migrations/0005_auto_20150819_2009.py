# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150817_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidrag',
            name='data',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bidrag',
            name='votes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compo',
            name='htmlContent',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='bidrag',
            name='file',
            field=models.FileField(upload_to=core.models.update_filename),
        ),
    ]
