# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150819_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidragFile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.update_filename)),
                ('time', models.DateTimeField(auto_now=True)),
                ('bidrag', models.ForeignKey(to='core.Bidrag')),
            ],
        ),
    ]
