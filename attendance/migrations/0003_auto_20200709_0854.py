# Generated by Django 3.0.7 on 2020-07-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20200629_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parade',
            name='commander_strength',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parade',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='parade',
            name='personnel_strength',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parade',
            name='total_strength',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
