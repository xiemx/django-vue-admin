# Generated by Django 3.1.5 on 2021-02-23 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0007_toolkitingresswhitelist_toolkitkubernetescleaner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolkitexam',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='toolkitexam',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]