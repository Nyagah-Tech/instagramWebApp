# Generated by Django 2.0 on 2020-01-05 13:28

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0007_auto_20200104_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='comments',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]