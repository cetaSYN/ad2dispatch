# Generated by Django 2.1.1 on 2019-01-25 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190125_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hidden',
        ),
    ]
