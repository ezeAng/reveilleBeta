# Generated by Django 3.0.7 on 2020-06-29 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parade',
            old_name='first_last',
            new_name='time_of_day',
        ),
    ]