# Generated by Django 2.0.5 on 2018-06-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecosyn', '0016_auto_20180610_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='illustration',
            old_name='X',
            new_name='height',
        ),
        migrations.RenameField(
            model_name='illustration',
            old_name='Y',
            new_name='width',
        ),
        migrations.AlterField(
            model_name='graphnode',
            name='liens',
            field=models.ManyToManyField(to='ecosyn.Lien'),
        ),
    ]
