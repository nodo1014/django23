# Generated by Django 3.2.18 on 2023-04-28 14:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0038_auto_20230426_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touritem',
            name='d_time1',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='d_time2',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='r_time1',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='r_time2',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
