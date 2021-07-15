# Generated by Django 3.2.5 on 2021-07-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0008_rename_is_installed_clientdevice_installed_through_the_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientdevice',
            name='device_invoice',
        ),
        migrations.AddField(
            model_name='clientdevice',
            name='device_invoice_or_manufacturer',
            field=models.FileField(default='file.pdf', upload_to='Client_Devices_Invoices_Manufacturer_Labels', verbose_name='Device Attachment'),
            preserve_default=False,
        ),
    ]
