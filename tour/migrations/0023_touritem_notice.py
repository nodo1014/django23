# Generated by Django 3.2.18 on 2023-04-24 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0022_alter_touritem_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='touritem',
            name='notice',
            field=models.TextField(blank=True),
        ),
    ]
