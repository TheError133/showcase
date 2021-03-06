# Generated by Django 3.1.5 on 2021-01-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0005_auto_20210129_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
    ]
