# Generated by Django 4.2.7 on 2023-12-15 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_app', '0003_remove_habit_pleasant_habit_habit_is_pleasant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='time_required',
            field=models.PositiveSmallIntegerField(default=120, verbose_name='time required in seconds'),
        ),
    ]