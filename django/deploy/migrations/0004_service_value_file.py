# Generated by Django 3.1.5 on 2021-02-23 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_release_value_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='value_file',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
