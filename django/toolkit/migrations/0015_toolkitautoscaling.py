# Generated by Django 3.1.5 on 2021-03-10 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toolkit', '0014_toolkitkubernetescleaner_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='toolKitAutoScaling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(blank=True, max_length=50, null=True)),
                ('service', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.IntegerField()),
                ('product', models.CharField(blank=True, max_length=50, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
