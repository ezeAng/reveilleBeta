# Generated by Django 3.0.8 on 2020-07-23 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_auto_20200723_0633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parade',
            old_name='disrepancy_override',
            new_name='ignore_discrepancy',
        ),
    ]
