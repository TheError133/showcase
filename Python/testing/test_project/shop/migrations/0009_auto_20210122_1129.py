# Generated by Django 3.1.5 on 2021-01-22 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210122_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='parameters',
            new_name='description',
        ),
    ]