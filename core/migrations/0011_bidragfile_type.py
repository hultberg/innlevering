# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150906_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidragfile',
            name='type',
            field=models.CharField(default='thebidrag', max_length=50),
        ),
    ]
