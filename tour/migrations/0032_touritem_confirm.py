# Generated by Django 3.2.18 on 2023-04-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0031_alter_iti_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='touritem',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
    ]
