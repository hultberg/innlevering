# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_innleveringuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='compo',
            name='isPublished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='compo',
            name='isVotingMode',
            field=models.BooleanField(default=False),
        ),
    ]
