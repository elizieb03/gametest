# Generated by Django 4.1.2 on 2023-03-01 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_completed',
        ),
    ]
