# Generated by Django 3.1.5 on 2021-01-29 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['section', 'name']},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='url',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='url',
            new_name='slug',
        ),
    ]
