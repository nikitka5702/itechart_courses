# Generated by Django 2.1.7 on 2019-03-14 14:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), null=True, size=None),
        ),
    ]
