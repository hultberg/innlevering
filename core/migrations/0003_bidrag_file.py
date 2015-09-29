# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_compo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidrag',
            name='file',
            field=models.FileField(default='', upload_to='test'),
            preserve_default=False,
        ),
    ]
