# Generated by Django 3.0.7 on 2020-07-15 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_auto_20200713_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='absence',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='parade',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='parade',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='status',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='status',
            name='updated_by',
        ),
    ]
