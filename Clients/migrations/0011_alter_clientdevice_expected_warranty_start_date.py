# Generated by Django 3.2.5 on 2021-07-15 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0010_rename_device_invoice_or_manufacturer_clientdevice_device_invoice_or_manufacturer_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdevice',
            name='expected_warranty_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Expected Warranty Start Date'),
        ),
    ]
