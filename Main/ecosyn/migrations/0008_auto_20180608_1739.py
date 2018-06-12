# Generated by Django 2.0.5 on 2018-06-08 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecosyn', '0007_auto_20180606_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lien',
            name='consequence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='causes', to='ecosyn.Sujet'),
        ),
        migrations.AlterField(
            model_name='lien',
            name='relative_share',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]