# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_bidragfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidrag',
            name='file',
        ),
        migrations.RemoveField(
            model_name='bidrag',
            name='fileLocation',
        ),
    ]
