# Generated by Django 2.1.1 on 2019-05-02 00:16

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteertype',
            name='common',
            field=models.BooleanField(default=False, help_text='Common type. If checked, will prevent the system from hiding the type after a week'),
        ),
        migrations.AddField(
            model_name='volunteertype',
            name='default',
            field=models.BooleanField(default=False, help_text='If checked, this type will be added to new events by default'),
        ),
        migrations.AlterField(
            model_name='event',
            name='types',
            field=models.ManyToManyField(default=events.models.default_types, to='events.VolunteerType'),
        ),
        migrations.AlterField(
            model_name='volunteertype',
            name='hidden',
            field=models.BooleanField(default=False, help_text='If checked, will only be shown to users with the view_hidden_events and vol_hidden_events permissions'),
        ),
        migrations.AlterField(
            model_name='volunteertype',
            name='instructions',
            field=models.TextField(help_text='Instructions given to volunteers of this type upon volunteering'),
        ),
        migrations.AlterField(
            model_name='volunteertype',
            name='max_volunteers',
            field=models.IntegerField(blank=True, help_text='Maximum volunteers allowed for an event', null=True),
        ),
        migrations.AlterField(
            model_name='volunteertype',
            name='type',
            field=models.CharField(help_text='Name of volunteer type', max_length=16, unique=True),
        ),
    ]
