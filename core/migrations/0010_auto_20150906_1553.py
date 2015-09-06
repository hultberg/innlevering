# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150906_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidrag',
            old_name='user',
            new_name='creator',
        ),
    ]
