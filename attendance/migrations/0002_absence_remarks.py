# Generated by Django 3.0.6 on 2020-05-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='remarks',
            field=models.TextField(default=None),
        ),
    ]