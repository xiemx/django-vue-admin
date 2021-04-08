# Generated by Django 3.1.5 on 2021-02-23 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0005_auto_20210223_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='release',
            name='rollback',
        ),
        migrations.AddField(
            model_name='release',
            name='revision',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='release',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
