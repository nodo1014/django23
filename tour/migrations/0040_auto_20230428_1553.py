# Generated by Django 3.2.18 on 2023-04-28 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0039_auto_20230428_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touritem',
            name='air_code',
            field=models.CharField(max_length=2, verbose_name='항공코드'),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='airline',
            field=models.CharField(blank=True, max_length=20, verbose_name='항공사'),
        ),
        migrations.AlterField(
            model_name='touritem',
            name='title',
            field=models.CharField(blank=True, max_length=50, verbose_name='상품명'),
        ),
        migrations.RenameModel(
            old_name='ShareItiName',
            new_name='AirBlockName',
        ),
        migrations.CreateModel(
            name='AirBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airblock_name', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.airblockname')),
                ('touritem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.touritem')),
            ],
        ),
    ]
