# Generated by Django 5.0.1 on 2024-02-10 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_event_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='winner',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
