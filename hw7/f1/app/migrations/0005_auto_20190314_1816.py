# Generated by Django 2.1.7 on 2019-03-14 15:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190314_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
    ]
