# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instasleuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='user_id_fk',
            field=models.ForeignKey(to='instasleuth.UserPoints', db_column=b'user_id'),
        ),
    ]
