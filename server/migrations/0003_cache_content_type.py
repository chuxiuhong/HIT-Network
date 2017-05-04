# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_cache'),
    ]

    operations = [
        migrations.AddField(
            model_name='cache',
            name='content_type',
            field=models.CharField(default='text/css', max_length=50),
            preserve_default=False,
        ),
    ]
