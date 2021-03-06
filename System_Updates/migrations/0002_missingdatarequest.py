# Generated by Django 3.2.5 on 2021-07-15 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System_Updates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissingDataRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(max_length=350, verbose_name='Data Type')),
                ('data_to_be_added', models.CharField(max_length=350, verbose_name='Data To Be Added')),
            ],
            options={
                'verbose_name': 'Missing Data Request',
                'verbose_name_plural': 'Missing Data Requests',
            },
        ),
    ]
