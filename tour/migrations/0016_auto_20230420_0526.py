# Generated by Django 3.2.18 on 2023-04-20 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0015_alter_detailcode_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='touritem',
            old_name='item_code',
            new_name='detail_code',
        ),
        migrations.AddField(
            model_name='touritem',
            name='code_suffix',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='airline',
            field=models.CharField(max_length=2),
        ),
    ]