# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instasleuth', '0002_auto_20171028_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='user_image_url',
            field=models.CharField(default=b'http://34.227.56.111/static/5.jpg', max_length=1000),
        ),
    ]
