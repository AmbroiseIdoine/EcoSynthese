# Generated by Django 2.0.5 on 2018-06-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecosyn', '0026_auto_20180612_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='link',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
