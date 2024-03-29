# Generated by Django 3.2.18 on 2023-04-28 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0041_remove_airblock_touritem'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='AirBlockName',
            new_name='Block',
        ),
        migrations.DeleteModel(
            name='AirBlock',
        ),
        migrations.AddField(
            model_name='blockitem',
            name='name',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.block'),
        ),
    ]
