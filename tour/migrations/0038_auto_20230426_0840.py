# Generated by Django 3.2.18 on 2023-04-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0037_auto_20230426_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touritem',
            name='share_air_chk',
            field=models.BooleanField(default=False, help_text='기본값 False'),
        ),
        migrations.DeleteModel(
            name='ShareIti',
        ),
    ]