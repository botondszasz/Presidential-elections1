# Generated by Django 5.0.1 on 2024-01-31 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_rename_hascandidated_profile_hasapplied'),
    ]

    operations = [
        migrations.CreateModel(
            name='displayUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
