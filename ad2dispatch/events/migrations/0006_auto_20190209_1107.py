# Generated by Django 2.1.1 on 2019-02-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190125_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteertype',
            name='type',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
