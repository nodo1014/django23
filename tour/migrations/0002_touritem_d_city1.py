# Generated by Django 3.2.18 on 2023-04-14 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='touritem',
            name='d_city1',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]