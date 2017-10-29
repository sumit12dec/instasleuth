# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_pan', models.CharField(max_length=100)),
                ('user_dob', models.CharField(max_length=100)),
                ('user_correction_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoints',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_points', models.IntegerField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='userdata',
            name='user_id_fk',
            field=models.ForeignKey(to='instasleuth.UserPoints'),
        ),
    ]
