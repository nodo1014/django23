# Generated by Django 3.2.18 on 2023-04-15 20:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0009_auto_20230415_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basiccode',
            name='detail_code',
        ),
        migrations.RemoveField(
            model_name='basiccode',
            name='title',
        ),
        migrations.AddField(
            model_name='basiccode',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, help_text='방콕/파타야 빠빠빠 상품', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detailcode',
            name='baskci_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tour.basiccode'),
        ),
        migrations.AlterField(
            model_name='basiccode',
            name='basic_code',
            field=models.CharField(help_text='예)ATP101', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='detailcode',
            name='detail_code',
            field=models.CharField(help_text='예)KE00 항공+숫자로 작성', max_length=4, unique=True),
        ),
    ]
