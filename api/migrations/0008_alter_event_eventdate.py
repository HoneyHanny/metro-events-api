# Generated by Django 5.0.3 on 2024-03-29 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_event_eventnumberofattendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventDate',
            field=models.DateField(),
        ),
    ]
