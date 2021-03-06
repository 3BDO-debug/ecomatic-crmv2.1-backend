# Generated by Django 3.2.5 on 2021-07-14 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Configurations', '0001_initial'),
        ('Storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_full_name', models.CharField(max_length=750, verbose_name='Client Full Name')),
                ('client_phone_number_1', models.CharField(max_length=750, verbose_name='Client Phone Number 1')),
                ('client_phone_number_2', models.CharField(max_length=750, verbose_name='Client Phone Number 2')),
                ('client_landline_number', models.CharField(max_length=750, verbose_name='Client Landline Number')),
                ('client_address_1', models.CharField(max_length=750, verbose_name='Client Address 1')),
                ('client_address_2', models.CharField(max_length=750, verbose_name='Client Address 2')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Added at')),
                ('client_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.clientcategory', verbose_name='Client Category')),
                ('client_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.city', verbose_name='Client City')),
                ('client_region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.region', verbose_name='Client Region')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='ClientDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_feeding_source', models.CharField(max_length=350, verbose_name='Device Feeding Source')),
                ('purchasing_date', models.DateField(verbose_name='Purchasing Date')),
                ('installation_date', models.DateField(verbose_name='Installation Date')),
                ('warranty_start_date', models.DateField(verbose_name='Warranty Start Date')),
                ('device_invoice', models.FileField(upload_to='Client_Devices_Invoices', verbose_name='Device Invoice')),
                ('in_warranty', models.BooleanField(default=True, verbose_name='In Warranty')),
                ('related_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.branch', verbose_name='Related Branch')),
                ('related_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Clients.client', verbose_name='Related Client')),
                ('related_distributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Configurations.distributor', verbose_name='Related Distributor')),
                ('related_storage_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Storage.item', verbose_name='Related Storage Item')),
            ],
            options={
                'verbose_name': 'Client Device',
                'verbose_name_plural': 'Client Devices',
            },
        ),
    ]
