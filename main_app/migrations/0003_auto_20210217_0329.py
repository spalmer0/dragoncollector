# Generated by Django 3.1.6 on 2021-02-17 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_feeding'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feeding',
            old_name='cat',
            new_name='dragon',
        ),
    ]
