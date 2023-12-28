# Generated by Django 4.2.7 on 2023-12-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_app', '0004_alter_habit_time_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.CharField(choices=[('hourly', 'Ежечасно'), ('daily', 'Ежедневно'), ('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')], default='daily', max_length=50, verbose_name='period'),
        ),
    ]