# Generated by Django 2.2 on 2019-04-15 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('del_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('01', 'Single answer'), ('02', 'Multiple answer')], default='01', max_length=2)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polls.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('value', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polls.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='polls.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polls.Question')),
            ],
        ),
    ]