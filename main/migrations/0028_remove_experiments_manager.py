# Generated by Django 5.2 on 2025-05-05 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_experiments_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiments',
            name='manager',
        ),
    ]
