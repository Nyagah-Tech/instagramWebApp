# Generated by Django 2.0 on 2020-01-04 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0005_auto_20200104_0751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='user',
        ),
    ]