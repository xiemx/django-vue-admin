# Generated by Django 3.1.5 on 2021-03-09 09:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0010_auto_20210309_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolkitkubernetescleaner',
            name='pod',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), default=[], size=None),
        ),
    ]
