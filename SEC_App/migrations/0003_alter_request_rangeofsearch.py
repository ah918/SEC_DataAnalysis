# Generated by Django 3.2.4 on 2021-06-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SEC_App', '0002_auto_20210615_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='rangeOfsearch',
            field=models.IntegerField(choices=[(0, '@ALKAHRABA OR @AlkahrabaCare'), (1, '@ALKAHRABA OR @AlkahrabaCare OR كلمة البحث'), (2, 'كلمة البحث')]),
        ),
    ]
