# Generated by Django 2.0.5 on 2018-06-10 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecosyn', '0013_auto_20180610_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='Page',
            new_name='page',
        ),
    ]
