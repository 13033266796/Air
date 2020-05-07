# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('city_name', models.CharField(max_length=10)),
                ('city_date', models.DateField()),
                ('city_AQI', models.DecimalField(max_digits=5, decimal_places=2)),
                ('city_PM2_5', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
    ]
