# Generated by Django 3.2.5 on 2021-07-03 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newfile',
            old_name='file',
            new_name='the_file',
        ),
    ]