# Generated by Django 2.0.5 on 2018-05-25 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='nickname',
        ),
    ]