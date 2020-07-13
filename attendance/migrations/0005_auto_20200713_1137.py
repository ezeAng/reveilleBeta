# Generated by Django 3.0.7 on 2020-07-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20200709_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parade',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personnel',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
