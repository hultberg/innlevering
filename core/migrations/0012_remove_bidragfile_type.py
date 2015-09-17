# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_bidragfile_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidragfile',
            name='type',
        ),
    ]
