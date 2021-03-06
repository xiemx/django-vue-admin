# Generated by Django 3.1.5 on 2021-02-23 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0004_service_value_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
