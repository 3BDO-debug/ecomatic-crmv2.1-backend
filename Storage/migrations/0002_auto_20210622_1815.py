# Generated by Django 3.2.4 on 2021-06-22 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Storage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='available_qty',
        ),
        migrations.RemoveField(
            model_name='item',
            name='item_price',
        ),
    ]
