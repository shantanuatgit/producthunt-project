# Generated by Django 2.2.13 on 2021-05-05 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
    ]
