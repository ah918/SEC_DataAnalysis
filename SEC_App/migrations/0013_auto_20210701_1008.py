# Generated by Django 3.2.4 on 2021-07-01 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEC_App', '0012_auto_20210701_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='true_end',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='true_start',
            field=models.TextField(null=True),
        ),
    ]