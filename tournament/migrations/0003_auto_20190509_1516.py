# Generated by Django 2.1.7 on 2019-05-09 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20190509_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='games_per_person2',
            new_name='games_per_person',
        ),
    ]