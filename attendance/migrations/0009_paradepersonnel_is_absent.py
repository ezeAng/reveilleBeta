# Generated by Django 3.0.8 on 2020-07-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20200722_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='paradepersonnel',
            name='is_absent',
            field=models.BooleanField(default=False),
        ),
    ]