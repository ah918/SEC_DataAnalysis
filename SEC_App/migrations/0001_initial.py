# Generated by Django 3.2.4 on 2021-06-15 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.TextField()),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('rangeOfsearch', models.IntegerField()),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('includeAll', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('tweet_id', models.TextField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('place', models.TextField()),
                ('tweet_text', models.TextField()),
                ('hashtags', models.TextField()),
                ('urls', models.TextField()),
                ('nlike', models.IntegerField()),
                ('nretweet', models.IntegerField()),
                ('nreply', models.IntegerField()),
                ('username', models.TextField()),
                ('name', models.TextField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SEC_App.request')),
            ],
        ),
    ]