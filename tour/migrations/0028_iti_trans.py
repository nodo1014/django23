# Generated by Django 3.2.18 on 2023-04-25 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0027_auto_20230424_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='iti',
            name='trans',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
