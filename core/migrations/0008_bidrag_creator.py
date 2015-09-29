# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150906_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidrag',
            name='creator',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
