# Generated by Django 3.2.18 on 2023-04-28 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0040_auto_20230428_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airblock',
            name='touritem',
        ),
    ]
