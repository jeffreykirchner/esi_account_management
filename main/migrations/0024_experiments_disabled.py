# Generated by Django 4.2.13 on 2024-05-13 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_profile_disabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
