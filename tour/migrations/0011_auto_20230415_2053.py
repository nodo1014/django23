# Generated by Django 3.2.18 on 2023-04-15 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0010_auto_20230415_2050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basiccode',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='detailcode',
            old_name='name',
            new_name='title',
        ),
    ]