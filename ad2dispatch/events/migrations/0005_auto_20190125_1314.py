# Generated by Django 2.1.1 on 2019-01-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_event_hidden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='volunteertype',
            options={'default_permissions': (), 'permissions': (('view_hidden_events', 'Can view hidden events'), ('vol_hidden_events', 'Can volunteer for hidden events'))},
        ),
        migrations.AddField(
            model_name='volunteertype',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]