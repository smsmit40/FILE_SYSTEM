# Generated by Django 3.2.5 on 2021-07-04 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_file_newfile_the_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newfile',
            name='the_file',
            field=models.FileField(upload_to='media/'),
        ),
    ]
