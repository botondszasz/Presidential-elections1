# Generated by Django 5.0.1 on 2024-02-10 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='event',
            name='winner',
            field=models.TextField(default='', max_length=500),
        ),
    ]
