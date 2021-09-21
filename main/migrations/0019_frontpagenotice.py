# Generated by Django 3.2.7 on 2021-09-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210910_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontPageNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_text', models.CharField(default='', max_length=1000, verbose_name='Subject Text')),
                ('body_text', models.CharField(default='', max_length=10000, verbose_name='Body Text')),
                ('enabled', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Login Page Notice',
                'verbose_name_plural': 'Login Page Notices',
            },
        ),
    ]
