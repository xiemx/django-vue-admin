# Generated by Django 3.1.5 on 2021-04-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0016_toolkitgraphitecleaner'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolkitautoscaling',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='toolkitexam',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='toolkitgraphitecleaner',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='toolkitingresswhitelist',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='toolkitkubernetescleaner',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
