# Generated by Django 2.0.5 on 2018-06-10 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecosyn', '0011_auto_20180610_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitle', models.CharField(blank=True, max_length=200)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GraphNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radius', models.FloatField()),
                ('X', models.FloatField()),
                ('Y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(blank=True, max_length=200)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='ecosyn/icons/')),
            ],
        ),
        migrations.CreateModel(
            name='Illustration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('L', 'Left'), ('R', 'Right'), ('BR', 'Bottom Right'), ('BL', 'Bottom Left'), ('BC', 'Bottom Center')], default='L', max_length=2)),
                ('code', models.TextField(blank=True, null=True)),
                ('X', models.FloatField()),
                ('Y', models.FloatField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='illustrations', to='ecosyn.Content')),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecosyn.Picture')),
            ],
        ),
        migrations.CreateModel(
            name='PictureDim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveSmallIntegerField()),
                ('opinion', models.BooleanField(default=False)),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecosyn.Picture')),
            ],
        ),
        migrations.RemoveField(
            model_name='graph',
            name='liens',
        ),
        migrations.RemoveField(
            model_name='graph',
            name='secteur',
        ),
        migrations.RemoveField(
            model_name='secteursection',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='secteursection',
            name='secteur',
        ),
        migrations.RemoveField(
            model_name='sujetsection',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='sujetsection',
            name='sujet',
        ),
        migrations.RemoveField(
            model_name='grapharrow',
            name='node',
        ),
        migrations.RemoveField(
            model_name='sujet',
            name='icon_size',
        ),
        migrations.RemoveField(
            model_name='sujet',
            name='icon_x',
        ),
        migrations.RemoveField(
            model_name='sujet',
            name='icon_y',
        ),
        migrations.AlterField(
            model_name='arrowbreak',
            name='arrow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breaks', to='ecosyn.GraphArrow'),
        ),
        migrations.AlterField(
            model_name='secteur',
            name='icon_picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='ecosyn.Icon'),
        ),
        migrations.AlterField(
            model_name='sujet',
            name='icon_picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='ecosyn.Icon'),
        ),
        migrations.DeleteModel(
            name='Graph',
        ),
        migrations.DeleteModel(
            name='SecteurSection',
        ),
        migrations.DeleteModel(
            name='SujetSection',
        ),
        migrations.AddField(
            model_name='section',
            name='secteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_set', to='ecosyn.Secteur'),
        ),
        migrations.AddField(
            model_name='section',
            name='sujet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_set', to='ecosyn.Sujet'),
        ),
        migrations.AddField(
            model_name='graphnode',
            name='illustration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graph', to='ecosyn.Illustration'),
        ),
        migrations.AddField(
            model_name='graphnode',
            name='liens',
            field=models.ManyToManyField(limit_choices_to={'cause': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ecosyn.Sujet')}, to='ecosyn.Lien'),
        ),
        migrations.AddField(
            model_name='graphnode',
            name='secteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecosyn.Secteur'),
        ),
        migrations.AddField(
            model_name='graphnode',
            name='sujet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ecosyn.Sujet'),
        ),
        migrations.AddField(
            model_name='content',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecosyn.Section'),
        ),
        migrations.AddField(
            model_name='grapharrow',
            name='node1',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='arrows', to='ecosyn.GraphNode'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grapharrow',
            name='node2',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ecosyn.GraphNode'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='dims',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecosyn.PictureDim'),
        ),
    ]