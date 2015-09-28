# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150927_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='innleveringuser',
            name='currenttimestamp',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='innleveringuser',
            name='currenttoken',
            field=models.TextField(default=''),
        ),
    ]
